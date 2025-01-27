from django.utils import timezone
from django.core.cache import cache
from django.db.models import Count, Avg
import secrets
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import WatchHistory
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from collections import defaultdict
from rest_framework.viewsets import ViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Content, Episode, Review
from .serializers import ContentSerializer, EpisodeSerializer, ReviewSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100
                    

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'age_rating']
    search_fields = ['title', 'cast', 'genres']
    ordering_fields = ['likes', 'title']

    def get_permissions(self):
        if self.action in ['watch', 'update_watch_progress', 'continue_watching']:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=['get'], url_path='watch')
    def watch(self, request, pk=None):
        content = self.get_object()
        user = request.user

        # watch history
        watch_history, created = WatchHistory.objects.get_or_create(
            user=user,
            content=content
        )
        watch_history.last_watched = timezone.now()
        watch_history.save()

       
        stream_token = secrets.token_urlsafe(32)
        cache.set(f'stream_token_{user.id}_{content.id}', stream_token, 3600)

        return Response({
            "title": content.title,
            "description": content.descriptions,
            "age_rating": content.age_rating,
            "category": content.category,
            "stream_url": f"{content.stream_url}?token={stream_token}",
            "duration": content.duration,
            "watch_progress": watch_history.watched_duration,
            "is_completed": watch_history.completed,
            "reactions": {
                "likes": content.likes,
                "dislikes": content.dislikes
            },
            "genres": content.genres
        })

    @action(detail=True, methods=['post'], url_path='update-progress')
    def update_watch_progress(self, request, pk=None):
        content = self.get_object()
        watched_duration = request.data.get('watched_duration', 0)
        completed = request.data.get('completed', False)

        watch_history, _ = WatchHistory.objects.get_or_create(
            user=request.user,
            content=content
        )
        watch_history.watched_duration = watched_duration
        watch_history.completed = completed
        watch_history.save()

        return Response({
            "success": True,
            "progress": watched_duration,
            "completed": completed
        })

    @action(detail=False, methods=['get'], url_path='continue-watching')
    def continue_watching(self, request):
        watch_history = WatchHistory.objects.filter(
            user=request.user,
            completed=False
        ).select_related('content').order_by('-last_watched')[:10]

        return Response([{
            "content_id": history.content.id,
            "title": history.content.title,
            "thumbnail": history.content.thumbnail_url,
            "progress_percentage": (history.watched_duration / history.content.duration) * 100,
            "last_watched": history.last_watched
        } for history in watch_history])

    @action(detail=True, methods=['post'], url_path='add-review')
    def add_review(self, request, pk=None):
        content = self.get_object()
        data = request.data
        
        if not all(key in data for key in ['rating', 'comment']):
            return Response(
                {"error": "Rating and comment are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            review = Review.objects.create(
                content=content,
                user=request.user,
                rating=data['rating'],
                comment=data['comment']
            )
            return Response(
                {"success": "Review added successfully!"}, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @method_decorator(cache_page(60 * 5))  
    @action(detail=False, methods=['get'], url_path='recommendations')
    def recommendations(self, request):
        top_content = Content.objects.filter(
            reactions__likes__gt=1000
        ).select_related(
            'category'
        ).prefetch_related(
            'genres'
        ).order_by('-reactions__likes')[:5]
        
        serializer = self.get_serializer(top_content, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='trailer')
    def trailer(self, request, pk=None):
        content = self.get_object()
        if not content.trailer_url:
            return Response(
                {"error": "No trailer available for this content"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            video_info = ffmpeg.probe(content.trailer_url)
            duration = float(video_info['streams'][0]['duration']) 
            formatted_duration = self.format_duration(duration)
        except ffmpeg.Error:
            raise NotFound("Trailer video duration could not be determined.")
        
        return Response({
            "title": content.title,
            "trailer_url": content.trailer_url,
            "duration": formatted_duration
        })

    @action(detail=False, methods=['get', 'post'], url_path='watchlist')
    def watchlist(self, request):
        if request.method == 'GET':
            watchlist = request.user.watchlist.select_related('category').all()
            serializer = ContentSerializer(watchlist, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            try:
                content_id = request.data.get('content_id')
                content = Content.objects.get(id=content_id)
                request.user.watchlist.add(content)
                return Response(
                    {"success": "Added to watchlist"},
                    status=status.HTTP_201_CREATED
                )
            except Content.DoesNotExist:
                return Response(
                    {"error": "Content not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

    @method_decorator(cache_page(60 * 5))  
    @action(detail=False, methods=['get'], url_path='trending')
    def trending(self, request):
        trending = Content.objects.select_related(
            'category'
        ).annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        ).order_by('-reactions__likes')[:5]
        
        serializer = self.get_serializer(trending, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 30)) 
    @action(detail=True, methods=['get'], url_path='episode-guide')
    def episode_guide(self, request, pk=None):
        content = self.get_object()
        if content.category != "TV Show":
            return Response(
                {"error": "Episode guide is only available for TV shows"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        episodes = Episode.objects.filter(
            content=content
        ).select_related(
            'content'
        ).order_by('season', 'episode_number')
        
        seasons = defaultdict(list)
        for episode in episodes:
            seasons[episode.season].append(EpisodeSerializer(episode).data)

        return Response({
            "title": content.title,
            "total_seasons": len(seasons),
            "seasons": [
                {
                    "season": season, 
                    "episode_count": len(episode_list),
                    "episodes": episode_list
                } 
                for season, episode_list in sorted(seasons.items())
            ]
        })


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['season', 'content']
    ordering_fields = ['episode_number', 'air_date']
    ordering = ['season', 'episode_number']

class AnalyticsViewSet(ViewSet):
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'], url_path='top-content')
    def top_content(self, request):
        top_content = Content.objects.order_by('-reactions__likes')[:10]
        serializer = ContentSerializer(top_content, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['content', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
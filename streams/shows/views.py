from django.utils import timezone
from django.core.cache import cache
from django.db.models import Count, Avg
import secrets
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
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
from .models import Series, Episode
from .serializers import SeriesSerializer, EpisodeSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    @action(detail=True, methods=['get'], url_path='watch')
    def watch(self, request, pk=None):
        content = self.get_object()
        user = request.user

        # Update watch history
        # watch_history, created = WatchHistory.objects.get_or_create(
        #     user=user,
        #     content=content
        # )
        # watch_history.last_watched = timezone.now()
        # watch_history.save()

        # Generate a signed URL for streaming
        signed_url = content.generate_signed_url()

        if not signed_url:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "title": content.title,
            "description": content.descriptions,
            "age_rating": content.age_rating,
            "category": content.category,
            "stream_url": signed_url,  # Use the signed URL
            "duration": content.duration,
            # "watch_progress": watch_history.watched_duration,
            # "is_completed": watch_history.completed,
            # "last_played": watch_history.last_watched,
            "reactions": {
                "likes": content.likes,
                "dislikes": content.dislikes
            },
            "genres": content.genres
        })
        
    # @action(detail=False, methods=['get'], url_path='continue-watching')
    # def continue_watching(self, request):
    #     watch_history = WatchHistory.objects.filter(
    #         user=request.user,
    #         completed=False
    #     ).select_related('content').order_by('-last_watched')[:10]

    #     return Response([{
    #         "content_id": history.content.id,
    #         "title": history.content.title,
    #         "thumbnail": history.content.thumbnail_url,
    #         "progress_percentage": (history.watched_duration / history.content.duration) * 100,
    #         "last_watched": history.last_watched
    #     } for history in watch_history])
        
    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        content = self.get_object()
        user = request.user
        action_type = request.data.get('action', 'like')  # 'like' or 'dislike'

        if action_type == 'like':
            content.likes += 1
        elif action_type == 'dislike':
            content.dislikes += 1
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        content.save()
        return Response({
            "success": f"{action_type.capitalize()} successful",
            "likes": content.likes,
            "dislikes": content.dislikes
        }, status=status.HTTP_200_OK)
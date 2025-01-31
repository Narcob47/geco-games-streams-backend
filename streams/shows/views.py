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
from .models import Series, Episode, ContinueWatching, Like, Dislike
from .serializers import SeriesSerializer, EpisodeSerializer

class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    @action(detail=True, methods=['get'], url_path='play')
    def play(self, request, pk=None):
        series = self.get_object()
        series.log_play_event()  # Log the play event
        signed_url = series.generate_signed_url()

        if not signed_url:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "title": series.title,
            "description": series.descriptions,
            "age_rating": series.age_rating,
            "category": series.category,
            "stream_url": signed_url,  # Use the signed URL
            "duration": series.duration,
            "reactions": {
                "likes": series.likes,
                "dislikes": series.dislikes
            },
            "genres": series.genres
        })

class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer

    @action(detail=True, methods=['get'], url_path='play')
    def play(self, request, pk=None):
        episode = self.get_object()
        signed_url = episode.generate_signed_url()

        if not signed_url:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "title": episode.title,
            "description": episode.description,
            "episode_number": episode.episode_number,
            "stream_url": signed_url,  # Use the signed URL
            "duration": episode.duration,
            "series": episode.series.title
        })

    @action(detail=True, methods=['post'], url_path='continue-watching')
    def continue_watching(self, request, pk=None):
        episode = self.get_object()
        user = request.user
        progress = request.data.get('progress', 0.0)

        continue_watching, created = ContinueWatching.objects.update_or_create(
            user=user,
            episode=episode,
            defaults={'progress': progress}
        )

        return Response({
            "message": "Continue watching updated",
            "progress": continue_watching.progress
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        episode = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(user=user, episode=episode)

        if created:
            episode.series.likes += 1
            episode.series.save()

        return Response({
            "message": "Episode liked",
            "likes": episode.series.likes
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='dislike')
    def dislike(self, request, pk=None):
        episode = self.get_object()
        user = request.user

        dislike, created = Dislike.objects.get_or_create(user=user, episode=episode)

        if created:
            episode.series.dislikes += 1
            episode.series.save()

        return Response({
            "message": "Episode disliked",
            "dislikes": episode.series.dislikes
        }, status=status.HTTP_200_OK)
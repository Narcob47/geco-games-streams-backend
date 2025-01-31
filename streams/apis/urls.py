from django.urls import path
from users.views import UserViewSet, UserProfileViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserProfileViewSet
from shows.views import SeriesViewSet, EpisodeViewSet
from movies.views import MovieViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list-create'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
    path('user-profiles/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='userprofile-list-create'),
    path('user-profiles/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='userprofile-detail'),
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('users/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    
    path('series/', SeriesViewSet.as_view({'get': 'list', 'post': 'create'}), name='content-list-create'),
    path('series/<int:pk>/', SeriesViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update','delete': 'destroy'}), name='content-detail'),
    path('series/<int:pk>/watch/', SeriesViewSet.as_view({'get': 'play'}), name='content-watch'),
    path('series/<int:pk>/like/', SeriesViewSet.as_view({'post': 'like'}), name='content-like'),
    path('episodes/', EpisodeViewSet.as_view({'get': 'list', 'post': 'create'}), name='episode-list-create'),
    path('episodes/<int:pk>/', EpisodeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='episode-detail'),
    path('episodes/<int:pk>/play/', EpisodeViewSet.as_view({'get': 'play'}), name='episode-play'),
    path('episodes/<int:pk>/continue-watching/', EpisodeViewSet.as_view({'post': 'continue_watching'}), name='episode-continue-watching'),
    path('episodes/<int:pk>/like/', EpisodeViewSet.as_view({'post': 'like'}), name='episode-like'),
    path('episodes/<int:pk>/dislike/', EpisodeViewSet.as_view({'post': 'dislike'}), name='episode-dislike'),
    
    path('movies/', MovieViewSet.as_view({'get': 'list', 'post': 'create'}), name='movie-list-create'),
    path('movies/<int:pk>/watch/', MovieViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='movie-detail'),
]
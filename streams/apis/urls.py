from django.urls import path
from users.views import UserViewSet, UserProfileViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserProfileViewSet
from shows.views import ContentViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list-create'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
    path('user-profiles/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='userprofile-list-create'),
    path('user-profiles/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='userprofile-detail'),
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('users/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('shows/', ContentViewSet.as_view({'get': 'list', 'post': 'create'}), name='content-list-create'),
    path('shows/<int:pk>/', ContentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='content-detail'),
    
    
    path('content/', ContentViewSet.as_view({'get': 'list', 'post': 'create'}), name='content-list-create'),
    path('content/<int:pk>/', ContentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='content-detail'),
    path('content/<int:pk>/watch/', ContentViewSet.as_view({'get': 'watch'}), name='content-watch'),
    path('content/continue-watching/', ContentViewSet.as_view({'get': 'continue_watching'}), name='content-continue-watching'),
    path('content/<int:pk>/like/', ContentViewSet.as_view({'post': 'like'}), name='content-like'),
    
    # path('episodes/', EpisodeViewSet.as_view({'get': 'list', 'post': 'create'}), name='episode-list-create'),
    # path('episodes/<int:pk>/', EpisodeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='episode-detail'),
    # path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list-create'),
    # path('reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='review-detail'),
    # path('analytics/', AnalyticsViewSet.as_view({'get': 'list'}), name='analytics-list'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserProfileViewSet, UserRegistrationViewSet, UserLoginViewSet
from .views import ContentViewSet, EpisodeViewSet, ReviewViewSet, AnalyticsViewSet

router = DefaultRouter()
router.register(r'content', ContentViewSet, basename='content')
router.register(r'episodes', EpisodeViewSet, basename='episodes')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register('analytics', AnalyticsViewSet, basename='analytics')



urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list-create'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
    path('user-profiles/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='userprofile-list-create'),
    path('user-profiles/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='userprofile-detail'),
    path('register/', UserRegistrationViewSet.as_view({'post': 'create'}), name='user-register'),
    path('login/', UserLoginViewSet.as_view({'post': 'create'}), name='user-login'),
]
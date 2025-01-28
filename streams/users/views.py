# views.py
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from .services import login_user, register_user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        result = login_user(username, password)

        if "message" in result:
            return Response(result, status=status.HTTP_200_OK)
        elif result["error"] == "User doesn't exist":
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        result = register_user(request.data)
        if "message" in result:
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
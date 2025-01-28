# services.py
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

def login_user(username, password):
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return {
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    elif not User.objects.filter(username=username).exists():
        return {"error": "User doesn't exist"}
    return {"error": "Invalid credentials"}

def register_user(data):
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return {"message": "User registered successfully"}
    return {"error": serializer.errors}
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer

User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    model = User
    permission_classes = []
    serializer_class = UserSerializer


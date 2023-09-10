from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    model = User
    permission_classes = []
    serializer_class = UserSerializer


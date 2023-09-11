from rest_framework import generics
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, UserRetrieveSerializer, ProfileSerializer, AddressSerializer
from .models import Profile, Address

User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    model = User
    permission_classes = []
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = UserRetrieveSerializer


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class AddressRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
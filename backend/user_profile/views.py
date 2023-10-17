from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, UserRetrieveSerializer, ProfileSerializer, AddressSerializer
from .models import Profile, Address

User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    model = User
    permission_classes = []
    serializer_class = UserSerializer

class APILogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({'status': 'OK, goodbye, all refresh tokens blacklisted'})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({'status': 'OK, goodbye'})


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

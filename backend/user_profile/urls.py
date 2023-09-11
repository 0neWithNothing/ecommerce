from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('user/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user_data'),
    path('user/<int:pk>/profile/', views.ProfileRetrieveUpdateAPIView.as_view(), name='user_profile'),
    path('user/<int:pk>/address/', views.AddressRetrieveUpdateAPIView.as_view(), name='user_address'),
    path('auth/signup/', views.UserCreateAPIView.as_view(), name='user_register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
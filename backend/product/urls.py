from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'size', views.SizeViewSet)
router.register(r'category', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
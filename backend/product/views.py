from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import GetProductSerializer, PostProductSerializer, SizeSerializer, CategorySerializer
from .models import Product, Size, Category


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return PostProductSerializer
        return GetProductSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


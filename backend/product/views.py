from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import (
    GetProductSerializer, PostProductSerializer, SizeSerializer,
    CategorySerializer, OrderItemSerializer, CartSerializer
)
from .models import Product, Size, Category, OrderItem, Cart


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


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = []


class CartRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
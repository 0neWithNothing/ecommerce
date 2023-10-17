from rest_framework import serializers

from .models import Product, Size, Category, OrderItem, Cart, Image

    
class SizeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=5)
    class Meta:
        model = Size
        fields = ('name',)
    

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    class Meta:
        model = Category
        fields = ('name',)
    

class ImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Image
        fields = '__all__'

class NestedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']

class GetProductSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField(many=True)
    category = serializers.StringRelatedField()
    images = NestedImageSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'


class PostProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'size', 'count', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'items', 'total_price']


class CheckoutSessionSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    class Meta:
        fields = ['cart_id']

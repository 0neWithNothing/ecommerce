from rest_framework import serializers

from .models import Product, Size, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
    
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
    
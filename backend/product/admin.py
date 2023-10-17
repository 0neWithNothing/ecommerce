from django.contrib import admin

from .models import Product, Image, Category, Size, OrderItem, Cart

# Register your models here.
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(OrderItem)
admin.site.register(Cart)

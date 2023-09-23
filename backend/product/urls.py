from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'sizes', views.SizeViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'order-items', views.OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pk>/images/', views.ImageListCreateAPIView.as_view(), name='product_images'),
    path('products/<int:pk>/images/<int:pk_img>/', views.ImageRetrieveDestroyAPIView.as_view(), name='image_detail'),
    path('cart/', views.CartRetrieveAPIView.as_view(), name='cart_data'),
    path('create-checkout-session/' , views.CreateCheckoutSessionAPIView.as_view()),
    # path('webhook-test/' , views.WebHook.as_view()),
]
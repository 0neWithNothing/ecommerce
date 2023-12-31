import stripe
from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializers import (
    GetProductSerializer, PostProductSerializer, SizeSerializer,
    CategorySerializer, OrderItemSerializer, CartSerializer,
    CheckoutSessionSerializer, ImageSerializer
)
from .models import Product, Size, Category, OrderItem, Cart, Image
from .permissions import IsAdminUserOrReadOnly, IsCartOwnerOrReadOnly


@method_decorator(cache_page(60*60, key_prefix="product-view"), name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related("images")
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return PostProductSerializer
        return GetProductSerializer


class ImageListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    def get_queryset(self):
        queryset = super(ImageListCreateAPIView, self).get_queryset()
        return queryset.filter(product__id=self.kwargs.get('pk'))


    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs.get("pk"))
        serializer.save(
            product=product
        )


class ImageRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = "pk_img"
    
    def get_queryset(self):
        queryset = super(ImageRetrieveDestroyAPIView, self).get_queryset()
        return queryset.filter(product__id=self.kwargs.get('pk'))
    
    def get_object(self):
        image = get_object_or_404(self.get_queryset(), pk=self.kwargs.get(self.lookup_field))
        return image


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class OrderItemViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsCartOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            cart=self.request.user.cart
        )


class CartRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    
    def get_object(self):
        cart = get_object_or_404(Cart, user=self.request.user.id)
        return cart
    

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
          request=CheckoutSessionSerializer,
          responses={301: None}
    )
    def post(self, request):
        cart = request.user.cart
        if not cart.items.all():
           return Response({"detail": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        if cart.total_price > 999999.99:
            return Response({"detail": "Total cost of your cart must be no more than $999,999.99"}, status=status.HTTP_400_BAD_REQUEST)
        
        line_items = []
        for item in cart.items.all():
            line_items.append({
                'price_data' :{
                    'currency' : 'usd',  
                        'product_data': {
                            'name': item.product.title,
                        },
                    'unit_amount': int(item.product.price*100)
                    },
                    'quantity' : item.count
            })
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode= 'payment',
                success_url= 'http://localhost:8000',
                cancel_url= 'http://localhost:8000',
                )
            return redirect(checkout_session.url , code=status.HTTP_302_FOUND)
        except Exception as e:
            print(e)
            return e


# class WebHook(APIView):
#   def post(self , request):
#     event = None
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']

#     try:
#       event = stripe.Webhook.construct_event(
#         payload ,sig_header , settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as err:
#         # Invalid payload
#         raise err
#     except stripe.error.SignatureVerificationError as err:
#         # Invalid signature
#         raise err

#     # Handle the event
#     if event.type == 'payment_intent.succeeded':
#       payment_intent = event.data.object 
#       print("--------payment_intent ---------->" , payment_intent)
#     elif event.type == 'payment_method.attached':
#       payment_method = event.data.object 
#       print("--------payment_method ---------->" , payment_method)
#     # ... handle other event types
#     else:
#       print('Unhandled event type {}'.format(event.type))

#     return Response({})

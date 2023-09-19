import stripe
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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
    CheckoutSessionSerializer
)
from .models import Product, Size, Category, OrderItem, Cart
from .permissions import IsAdminUserOrReadOnly


@method_decorator(cache_page(60*60, key_prefix="product-view"), name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

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
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
import stripe
from decimal import Decimal
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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
    

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionAPIView(APIView):
    def post(self, request):
        cart = Cart.objects.get(id=request.data.get('cart_id'))
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
                line_items=line_items,
                mode= 'payment',
                success_url= 'http://localhost:8000',
                cancel_url= 'http://localhost:8000',
                )
            return redirect(checkout_session.url , code=303)
        except Exception as e:
            print(e)
            return e
        

class WebHook(APIView):
  def post(self , request):
    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
      event = stripe.Webhook.construct_event(
        payload ,sig_header , settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as err:
        # Invalid payload
        raise err
    except stripe.error.SignatureVerificationError as err:
        # Invalid signature
        raise err

    # Handle the event
    if event.type == 'payment_intent.succeeded':
      payment_intent = event.data.object 
      print("--------payment_intent ---------->" , payment_intent)
    elif event.type == 'payment_method.attached':
      payment_method = event.data.object 
      print("--------payment_method ---------->" , payment_method)
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event.type))

    return Response({})
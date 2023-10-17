import json
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from google_login_server_flow.service import get_tokens_for_user


from product.models import Product, Cart, OrderItem
from product.serializers import (
    GetProductSerializer, PostProductSerializer,
    CartSerializer
)

User = get_user_model()

class AuthorizedMixin(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(email="shiz@shiz.com", password="qweasdzxc22")
        self.jwt_tokens = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.jwt_tokens["access"])


class TestProduct(AuthorizedMixin):

    endpoint = "/products/"

    # def test_product_unauthorized(self):
    #     self.client.credentials(user=None, token=None)
    #     response = self.client.get(self.endpoint)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_get(self):
        baker.make(Product, _quantity=3, make_m2m=True)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 3)
    
    def test_product_post(self):
        product = baker.prepare(Product, price=9999.99, id=1, _fill_optional=True)
        expected_json = PostProductSerializer(product).data
        response = self.client.post(self.endpoint, data=expected_json, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_json)

    def test_product_retrieve(self):
        product = baker.make(Product, price=9999.99, make_m2m=True, _fill_optional=True)
        expected_json = GetProductSerializer(product).data
        response = self.client.get(self.endpoint+str(product.id)+"/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_json)

    def test_product_update(self):
        product = baker.make(Product, price=9999.99, make_m2m=True, _fill_optional=True)
        expected_json = PostProductSerializer(product).data
        expected_json["title"] = "Updated Title"
        response = self.client.put(self.endpoint+str(product.id)+"/", data=expected_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")
    
    def test_product_partial(self):
        product = baker.make(Product, price=9999.99, make_m2m=True, _fill_optional=True)
        json_to_change = {
            "title": "Updated Title"
        }
        response = self.client.put(self.endpoint+str(product.id)+"/", data=json_to_change)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")
        
    def test_product_delete(self):
        product = baker.make(Product, price=9999.99, make_m2m=True, _fill_optional=True)
        response = self.client.delete(self.endpoint+str(product.id)+"/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        

class TestOrderItem(AuthorizedMixin):
    
    endpoint = "/cart/"

    def test_cart(self):
        cart = Cart.objects.get(user=self.user)
        expected_json = CartSerializer(cart).data
        response = self.client.get(reverse('cart_data'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_json)


class TestCheckout(AuthorizedMixin):

    endpoint = "/create-checkout-session/"

    def test_create_checkout_session(self):
        product = baker.make(Product, price=9999.99, make_m2m=True, _fill_optional=True)
        product2 = baker.make(Product, price=9999.99, make_m2m=True, _fill_optional=True)
        baker.make(OrderItem, cart=self.user.cart, product=product, make_m2m=True, _fill_optional=True)
        baker.make(OrderItem, cart=self.user.cart, product=product2, count=10, make_m2m=True, _fill_optional=True)
        response = self.client.post(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


    def test_create_checkout_session_with_empty_cart(self):
        response = self.client.post(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

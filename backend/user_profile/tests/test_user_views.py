from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from google_login_server_flow.service import get_tokens_for_user


from user_profile.models import Profile, Address

User = get_user_model()

class AuthorizedMixin(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(email="shiz@shiz.com", password="qweasdzxc22")
        self.jwt_tokens = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.jwt_tokens["access"])



class TestUser(APITestCase):

    def test_register_user(self):
        user_json = {
            "email": "test@test.test",
            "password": "qweasdzxc22",
            "password2": "qweasdzxc22",
        }
        response = self.client.post("/auth/signup/", data=user_json, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all()[0].email, user_json["email"])
    
    def test_retrieve_user(self):
        user = baker.make(User)
        response = self.client.get(f"/user/{user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)

    def test_profile_on_user_create(self):
        self.assertEqual(Profile.objects.count(), 0)
        baker.make(User)
        self.assertEqual(Profile.objects.count(), 1)
    
    def test_address_on_user_create(self):
        self.assertEqual(Address.objects.count(), 0)
        baker.make(User)
        self.assertEqual(Address.objects.count(), 1)

    def test_retrieve_profile(self):
        user = baker.make(User)
        response = self.client.get(f"/user/{user.id}/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], user.id)
    
    def test_retrieve_address(self):
        user = baker.make(User)
        response = self.client.get(f"/user/{user.id}/address/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], user.id)
    
    def test_update_profile(self):
        user = baker.make(User)
        expected_json = {
            "first_name": "test first name"
        }
        response = self.client.put(f"/user/{user.id}/profile/", data=expected_json, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], expected_json["first_name"])
    
    def test_update_address(self):
        user = baker.make(User)
        expected_json = {
            "country": "test country"
        }
        response = self.client.put(f"/user/{user.id}/address/", data=expected_json, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country"], expected_json["country"])


    def test_get_jwt_tokens(self):
        user_json = {
            "email": "test@test.test",
            "password": "qweasdzxc22",
        }
        User.objects.create_user(**user_json)
        response = self.client.post("/auth/token/", data=user_json, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_jwt_tokens(self):
        user_json = {
            "email": "test@test.test",
            "password": "qweasdzxc22",
        }
        User.objects.create_user(**user_json)
        tokens = self.client.post("/auth/token/", data=user_json, format="json").data
        response = self.client.post("/auth/token/refresh/", data={"refresh": tokens["refresh"]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(tokens["access"], response.data["access"])
        self.assertNotEqual(tokens["refresh"], response.data["refresh"])
        
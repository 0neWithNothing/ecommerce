from rest_framework import status
from rest_framework.test import APITestCase


class TestOauth(APITestCase):
    
    endpoint = "/oauth/google/"

    def test_google_redirect(self):
        response = self.client.get(self.endpoint+"redirect/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

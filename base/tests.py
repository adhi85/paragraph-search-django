from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from base.models import User, Paragraph, Word
from base.serializers import UserSerializer


class CreateUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "testpassword",
        }
        self.invalid_user_data = {
            "email": "invalidemail",
            "name": "",
            "password": "short",
        }

    def test_create_valid_user(self):
        response = self.client.post(reverse("create_user"), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = self.client.post(reverse("create_user"), data=self.invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateParasTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="test@example.com", name="Test User")
        self.client.force_authenticate(user=self.user)
        self.paras_data = {
            "para": "This is a test paragraph.\n\nThis is another paragraph."
        }

    def test_create_paras(self):
        response = self.client.post(reverse("create_paras"), data=self.paras_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Paragraph.objects.count(), 2)
        self.assertEqual(Word.objects.count(), 9)  # Number of words in the paragraphs

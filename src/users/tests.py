from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('users-api:register')
        data = {
            'username': 'john_doe',
            'first_name': 'john',
            'last_name': 'doe',
            'email': 'john@example.com',
            'password': '123456'
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'john_doe')
        
        # response = self.client.get('/users/4/')
        # self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})
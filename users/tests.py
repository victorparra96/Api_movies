# Django
from django.test import TestCase

# Python
import tempfile
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        user = User(
            email='testing_login@cosasdedevs.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )
        user.set_password('admin123')
        user.save()

    def test_login_user(self):

        client = APIClient()
        response = client.post(
                '/users/login/', {
                'email': 'testing_login@cosasdedevs.com',
                'password': 'admin123',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        result = json.loads(response.content)
        self.assertIn('access_token', result)
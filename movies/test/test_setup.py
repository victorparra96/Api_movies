# Django
from django.test import TestCase

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient

# Models
from movies.models import Movies
from users.models import User
from movies.models.comments import Comment


class TestSetUp(TestCase):

    def setUp(self):
        # Create model for user
        user = User(
                    email='testing_login@cosasdedevs.com',
                    first_name='Testing',
                    last_name='Testing',
                    username='testing_login'
                )
        user.set_password('admin123')
        user.save()

        # Create model for movies
        self.movie = Movies.objects.create(
            name='titanic',
            gender='AC',
            author='leonardo',
            production='netflix',
            duration='01:30:00',
            date_launch='1997-10-19',
            user=user
        )

        self.movie = Movies.objects.create(
            name='titanic 2.0',
            gender='SE',
            author='leonardo',
            production='netflix',
            duration='02:30:00',
            date_launch='1977-10-19',
            user=user
        )

        # Create model for comment
        self.comment = Comment.objects.create(
            user=user,
            movie=self.movie,
            description="sdfsdfsdfsdfdsfsdfdfsffsdf"
        )

        # Login
        client = APIClient()
        response = client.post(
                '/users/login/', {
                'email': 'testing_login@cosasdedevs.com',
                'password': 'admin123',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user

        # Authenticacion
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        return super().setUp()
# Django
from django.test import TestCase

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

# Views
from movies.views import calculate_average

# Models
from movies.models import Movies, Ranking
from users.models import User


class RankingTestCase(TestCase):

    def setUp(self):

        # Create model for user
        user = User(
                email='testing_login@prueba.com',
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

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

    def test_create_ranking(self):

        ranking = {
            'value': '4',
        }

        response = self.client.post(
            '/ranking/', 
            ranking,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """ def test_calculate_average_ranking(self):

        ranking = Ranking.objects.create(
            value=4,
            user=self.user,
            movie=self.movie
        )

        ranking = Ranking.objects.create(
            value=5,
            user=self.user,
            movie=self.movie
        )

        data = Ranking.objects.filter(movie=self.movie).value_list('value')
        average = calculate_average(data)

        self.assertTrue(average > 0) """






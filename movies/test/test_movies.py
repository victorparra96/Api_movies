# Python
import json

# Django Rest Framework
from rest_framework import status

# Models
from movies.models import Movies

# setup test
from movies.test.test_setup import TestSetUp


class MoviesTestCase(TestSetUp):

    def test_create_movie(self):

        movie = {
            'name': 'titanic',
            'gender': 'AC',
            'author': 'leonardo',
            'production': 'netflix',
            'duration': '01:30:00',
            'date_launch': '1997-10-19'
        }

        response = self.client.post(
            '/movies/', 
            movie,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_partial_movie(self):

        movie_update = {
            'name': 'titanic 2.0',
            'author': 'victor'
        }

        response = self.client.patch(
            f'/movies/{self.movie.pk}/', 
            movie_update,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_movie(self):

        movie_update = {
            'name': 'titanic 2.0',
            'gender': 'SE',
            'author': 'victor',
            'production': 'youtube',
            'duration': '02:30:00',
            'date_launch': '1998-10-19',
            'user': f'{self.user.pk}'
        }

        response = self.client.put(
            f'/movies/{self.movie.pk}/', 
            movie_update,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_movie(self):

        response = self.client.delete(
            f'/movies/{self.movie.pk}/',
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        movie_exists = Movies.objects.filter(pk=self.movie.pk)
        self.assertFalse(movie_exists)

    def test_get_movie(self):

        response = self.client.get('/movies/')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['count'], 2)
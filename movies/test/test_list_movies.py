# Python
import json

# Django Rest Framework
from rest_framework import status

# Models
from movies.models.list_movies import List_movie

# setup test
from movies.test.test_setup import TestSetUp


class ListMoviesTestCase(TestSetUp):

    def test_create_list_movie(self):

        list_movie = {
            'user': ''.format(self.user),
            'movie': self.movie.pk,
        }

        response = self.client.post(
            '/list_movies/', 
            list_movie,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_inactive_list_movie(self):

        list_movie = List_movie.objects.create(
            user=self.user,
            movie=self.movie
        )

        response = self.client.delete(
            '/list_movies/{}/'.format(list_movie.pk),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_movie_exists = List_movie.objects.filter(pk=list_movie.pk, is_active=False)
        self.assertTrue(list_movie_exists)

    def test_active_list_movie(self):

        list_movie = {
            'user': ''.format(self.user),
            'movie': self.movie.pk,
            'is_active': ''.format(True)
        }

        list_movie2 = List_movie.objects.create(user=self.user, movie=self.movie, is_active=False)

        response = self.client.post(
            '/list_movies/', 
            list_movie,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        list_movies_exists = List_movie.objects.filter(
            user=self.user, 
            movie=self.movie,
            is_active=True
        )
        self.assertTrue(list_movies_exists)

    def test_get_list_movie(self):

        list_movies = List_movie.objects.create(
            user=self.user, 
            movie=self.movie,
            is_active=True
        )

        response = self.client.get('/list_movies/')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['count'], 1)

        
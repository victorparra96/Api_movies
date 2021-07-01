# Python
import json

# Django Rest Framework
from rest_framework import status

# setup test
from movies.test.test_setup import TestSetUp


class RankingTestCase(TestSetUp):

    def test_create_ranking(self):

        ranking = {
            'user': ''.format(self.user),
            'movie': ''.format(self.movie),
            'value': 4,
        }

        response = self.client.post(
            '/movies/{}/rankings/'.format(self.movie.pk), 
            ranking,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)






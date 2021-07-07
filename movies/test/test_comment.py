# Python
import json

# Django Rest Framework
from rest_framework import status

# Models
from movies.models.comments import Comment

# setup test
from movies.test.test_setup import TestSetUp


class CommentTestCase(TestSetUp):

    def test_create_comment(self):

        comment = {
            'user': ''.format(self.user),
            'movie': ''.format(self.movie),
            'description': "hola que mas",
        }

        response = self.client.post(
            '/movies/{}/comment/'.format(self.movie.pk), 
            comment,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reply_comment(self):

        comment = {
            'user': ''.format(self.user),
            'movie': ''.format(self.movie),
            'description': "hola que mas",
            'reply': ''.format(self.comment.pk)
        }

        response = self.client.post(
            '/movies/{}/comment/'.format(self.movie.pk), 
            comment,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_inactive_comment(self):

        comment = Comment.objects.create(
            user=self.user,
            movie=self.movie,
            description="sdfsdfsdfsdfdsfsdfdfsffsdf"
        )

        response = self.client.delete(
            '/movies/{}/comment/{}/'.format(self.movie.pk, comment.pk),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        comment_exists = Comment.objects.filter(pk=comment.pk, is_active=False)
        self.assertTrue(comment_exists)

    def test_get_comment_for_movie(self):

        response = self.client.get('/movies/{}/comment/'.format(self.movie.pk))
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['count'], 1)
# Python
import json

# Django Rest Framework
from rest_framework import status

# Models
from movies.models.like import Like
from movies.models.comments import Comment

# setup test
from movies.test.test_setup import TestSetUp


class LikeTestCase(TestSetUp):

    def test_create_like(self):
        
        like = {
            'user': ''.format(self.user),
            'comment': ''.format(self.comment.pk),
        }

        response = self.client.post(
            '/comment/{}/like/'.format(self.comment.pk), 
            like,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_active_like(self):

        like = {
            'user': ''.format(self.user),
            'comment': ''.format(self.comment.pk),
            'is_active': ''.format(True)
        }

        like2 = Like.objects.create(
            user=self.user,
            comment=self.comment,
            is_active=False
        )

        response = self.client.post(
            '/comment/{}/like/'.format(self.comment.pk), 
            like,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        like_exists = Like.objects.filter(
            user=self.user,
            comment=self.comment,
            is_active=True
        )

        like_count = Like.objects.all().count()

        self.assertTrue(like_exists)
        self.assertEqual(like_count, 1)

    def test_inactive_like(self):

        like = Like.objects.create(
            user=self.user,
            comment=self.comment
        )

        response = self.client.delete(
            '/comment/{}/like/{}/'.format(self.comment.pk, like.pk),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        like_exists = Like.objects.filter(pk=like.pk, is_active=False)
        like_count = Like.objects.all().count()

        self.assertTrue(like_exists)
        self.assertEqual(like_count, 1)

    def test_get_like_for_comment(self):

        like = Like.objects.create(
            user=self.user,
            comment=self.comment
        )

        response = self.client.get('/comment/{}/like/'.format(self.comment.pk))
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['count'], 1)

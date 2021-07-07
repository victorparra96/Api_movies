"""Like model"""

# Django
from django.db import models

# Utils
from movies.utils.models import MovieModel


class Like(MovieModel):
    comment = models.ForeignKey('movies.Comment', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.comment.pk, self.user.username)
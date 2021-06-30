"""Like model"""

# Django
from django.db import models

# Utils
from movies.utils.models import MovieModel


class Like(MovieModel):
    comment = models.ForeignKey('movies.Comment', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return '{} at {}'.format(self.pk, self.comment)
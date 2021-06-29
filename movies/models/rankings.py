"""Ranking model"""

# Django
from django.db import models

# Utils
from movies.utils.models import MovieModel


class Ranking(MovieModel):
    value_choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movies', on_delete=models.CASCADE)
    value = models.IntegerField(choices=value_choices)

    def __str__(self):
        return f'{self.movie.name} {self.pk}'
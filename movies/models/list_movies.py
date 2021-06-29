"""List_movies model"""

# Django
from django.db import models

# Utils
from movies.utils.models import MovieModel


class List_movie(MovieModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movies', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.movie.name} {self.user.username} {self.pk}'
"""Comments model"""

# Django
from django.db import models

# django-ckeditor
from ckeditor.fields import RichTextField

# Utils
from movies.utils.models import MovieModel


class Comment(MovieModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movies', on_delete=models.CASCADE)
    description = RichTextField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.movie.name} {self.user.username} {self.pk}'
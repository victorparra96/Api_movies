# Django REST Framework
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

# Model
from movies.models import List_movie
from movies.models.movies import Movies

# Utils
from movies.utils.methods import validate_if_user_add_message


class ListMoviesModelSerializer(serializers.ModelSerializer):
    """List_movies Model Serializer"""

    user = serializers.StringRelatedField()
    movie = serializers.StringRelatedField()

    class Meta:
        """Meta class."""

        model = List_movie
        fields = (
            '__all__'
        )

class AddListMoviesSerializer(serializers.Serializer):
    """
    Add list_movies serializers.
    Handle the addition of a new movie to a list_movie.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    movie = serializers.IntegerField()

    def validate(self, data):
        """Validate if the user added a movie"""
        user = data['user']
        movie = data['movie']
        query = List_movie.objects.select_related().filter(user=user, movie=movie, is_active=True)
        validate_if_user_add_message(query, "list_movie")
        return data

    def create(self, data):
        """
        Create or update a new list_movie
        """

        user = data['user']
        # Get a movie instance
        movie = get_object_or_404(Movies, pk=data['movie'])

        # If list_movie exists with user=user & movie=movie & is_active=False
        # then update is_active=True
        # Else create new list_movie with user=user & movie=movie & is_active=True
        list_movie, created = List_movie.objects.update_or_create(
            user=user,
            movie=movie,
            is_active=False,
            defaults={'is_active': 'True'}
        )

        return list_movie

        
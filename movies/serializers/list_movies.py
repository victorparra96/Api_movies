# Django REST Framework
from rest_framework import serializers

# Model
from movies.models import List_movie

# Utils
from movies.utils import methods


class ListMoviesModelSerializer(serializers.ModelSerializer):
    """List_movies Model Serializer"""

    class Meta:
        """Meta class."""

        model = List_movie
        fields = (
            '__all__'
        )

class AddListMoviesSerializer(serializers.Serializer):
    """
    Add list_movies serializers.
    Handle the addition of a new ranking to a movie.
    Movie object must be provided in the context
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        """Validate if the user added a movie"""

        user = data
        movie = self.context['movie']
        methods.validate_if_user_add(List_movie, user, movie, "List_movie")
        return data

    def create(self, data):
        """
        Create a new list_movie
        using method the utils for validation
        """

        user = data
        movie = self.context['movie']

        list_movie = List_movie.objects.create(
            user=user,
            movie=movie,
            is_active=True
        )

        return list_movie

        
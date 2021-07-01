# Django REST Framework
from movies.models import movies
from movies.models.movies import Movies
from rest_framework import serializers

# Model
from movies.models import Ranking

# Utils
from movies.utils import methods


class RankingModelSerializer(serializers.ModelSerializer):
    """Ranking Model Serializer"""

    class Meta:
        """Meta class."""

        model = Ranking
        fields = (
            '__all__'
        )

class AddRankingSerializer(serializers.Serializer):
    """
    Add ranking serializer.
    Handle the addition of a new ranking to a movie.
    Movie object must be provided in the context
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    value = serializers.DecimalField(max_digits=2, decimal_places=1)

    def validate(self, data):
        """Validate if the user added a ranking"""

        user = data['user']
        movie = self.context['movie']
        methods.validate_if_user_add(Ranking, user, movie, "Ranking")
        return data

    def create(self, data):
        """
        Crate a new Raking and update calculate
        field raking_movie in movie.
        using method the utils for validation. 
        """

        user = data['user']
        movie = self.context['movie']

        ranking = Ranking.objects.create(
            user=user,
            movie=movie,
            value=data['value']
        )

        # Update movies in column ranking
        query = Ranking.objects.filter(movie=movie).values_list('value')
        average = sum(map(sum, list(query)))/len(query)
        movie.ranking_movie = average
        movie.save()

        return ranking
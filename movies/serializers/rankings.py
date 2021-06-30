# Django REST Framework
from movies.models.movies import Movies
from rest_framework import serializers

# Model
from movies.models import Ranking


class RankingModelSerializer(serializers.ModelSerializer):
    """Ranking Model Serializer"""

    class Meta:
        """Meta class."""

        model = Ranking
        fields = (
            '__all__'
        )

class AddRankingSerializer(serializers.Serializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    value = serializers.IntegerField()

    def validate_add_only_once(self, data):
        user = data['user']
        movie = data['movie']
        query = Ranking.objects.filter(user=user, movie=movie)
        if query.exists():
            raise serializers.ValidationError('User is already vote one movie once')
        return data

    def create(self, data):
        ranking = Ranking.objects.create(**data)

        # Update movies in column ranking
        query = Ranking.objects.filter(movie=data['movie']).values_list('value', flat=True)
        average = sum(query)/len(query)

        movie = self.context['movie']
        movie.ranking = average

        return ranking
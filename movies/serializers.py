# Python
from datetime import timedelta

# Django
from django.core.validators import FileExtensionValidator

# Django REST Framework
from rest_framework import serializers

# Model
from movies.models import Movies

class MoviesModelSerializer(serializers.ModelSerializer):
    """Movies Model Serializer"""

    class Meta:
        """Meta class."""

        model = Movies
        fields = (
            '__all__'
        )

class MoviesSerializer(serializers.Serializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(max_length=30)
    gender = serializers.CharField(max_length=2)
    author = serializers.CharField(max_length=30)
    production = serializers.CharField(max_length=30)
    image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], 
        required=False
    )
    duration = serializers.DurationField()
    date_launch = serializers.DateField()
    description = serializers.CharField(max_length=1000, required=False)

    def validate(self, data):

        image = None
        if 'photo' in data:
            image = data['photo']

        if image:
            if image.size > (512 * 1024):
                raise serializers.ValidationError(f"La imagen es demasiado grande, el peso máximo permitido es de 512KB y el tamaño enviado es de {round(image.size / 1024)}KB")

        return data

    def create(self, data):
        movies = Movies.objects.create(**data)
        return movies
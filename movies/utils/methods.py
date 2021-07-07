# Django REST Framework
from rest_framework import serializers


def validate_if_user_add(object:object, user, model, message:str):
    query = object.objects.filter(user=user, movie=model)
    if query.exists():
        raise serializers.ValidationError(f'User is already added {message}')
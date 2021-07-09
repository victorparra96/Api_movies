# Django REST Framework
from django.db.models.query import QuerySet
from rest_framework import serializers


def validate_if_user_add(object:object, user, model, message:str):
    query = object.objects.select_related().filter(user=user, movie=model)
    if query.exists():
        raise serializers.ValidationError(f'User is already added {message}')

def validate_if_user_add_message(query:QuerySet, message:str):
    if query.exists():
        raise serializers.ValidationError(f'User is already added {message}')
# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from movies.serializers import (MoviesModelSerializer, MoviesSerializer)

# Models
from movies.models import Movies

class MoviesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = MoviesModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender']

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        queryset = Movies.objects.all()
        return queryset

        
    def create(self, request, *args, **kwargs):
        serializer = MoviesSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        exp = serializer.save()
        data = MoviesModelSerializer(exp).data
        return Response(data, status=status.HTTP_201_CREATED)
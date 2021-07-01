"""List_movies views"""

# Django Rest Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from movies.models.list_movies import List_movie

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from movies.serializers.list_movies import ListMoviesModelSerializer, AddListMoviesSerializer


class ListMovieViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """List_Movie view set"""

    serializer_class = ListMoviesModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the list_movie exists"""
        pk = kwargs['slug_name']
        self.list_movie = get_object_or_404(List_movie, pk=pk)
        return super(ListMovieViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = List_movie.objects.all()
        return queryset

    def perform_destroy(self, instance):
        """Disable list_movie"""
        instance.is_active = False
        instance.save()

    def create(self, request, *args, **kwargs):
        serializer = AddListMoviesSerializer(
            data=request.data, 
            context={'list_movie': self.list_movie, "request": self.request})
        serializer.is_valid(raise_exception=True)
        list_movie = serializer.save()
        data = ListMoviesModelSerializer(list_movie).data
        return Response(data, status=status.HTTP_201_CREATED)
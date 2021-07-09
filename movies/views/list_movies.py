"""List_movies views"""

# Django Rest Framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

# Models
from movies.models.list_movies import List_movie
from movies.models.movies import Movies

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from movies.serializers.list_movies import ListMoviesModelSerializer, AddListMoviesSerializer


class ListMovieViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """List_Movie view set"""

    serializer_class = ListMoviesModelSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Get a list movies for user"""
        queryset = List_movie.objects.select_related().filter(user=self.request.user, is_active=True)
        return queryset

    def perform_destroy(self, instance):
        """Disable list_movie"""
        instance.is_active = False
        instance.save()

    def create(self, request, *args, **kwargs):
        serializer = AddListMoviesSerializer(
            data=request.data, 
            context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        list_movie = serializer.save()
        data = ListMoviesModelSerializer(list_movie).data
        return Response(data, status=status.HTTP_201_CREATED)
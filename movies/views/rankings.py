"""Ranking views"""

# Django Rest Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from movies.models import Movies

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from movies.serializers.rankings import RankingModelSerializer, AddRankingSerializer


class RankingViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Ranking view set"""

    serializer_class = RankingModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the movie exists"""
        pk = kwargs['slug_name']
        self.movie = get_object_or_404(Movies, pk=pk)
        return super(RankingViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = AddRankingSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        ranking = serializer.save()
        data = RankingModelSerializer(ranking).data
        return Response(data, status=status.HTTP_201_CREATED)
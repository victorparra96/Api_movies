"""Comment views"""

# Django Rest Framework
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from movies.models.movies import Movies
from movies.models.comments import Comment

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from movies.serializers.comments import CommentModelSerializer, AddCommentSerializer


class CommentViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Comment view set"""

    serializer_class = CommentModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the movie exists"""
        pk = kwargs['slug_name']
        self.movie = get_object_or_404(Movies, pk=pk)
        return super(CommentViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Comment.objects.filter(movie=self.movie, is_active=True)
        return queryset

    def perform_destroy(self, instance):
        """Disable comment"""
        instance.is_active = False
        instance.save()

    def create(self, request, *args, **kwargs):
        serializer = AddCommentSerializer(
            data=request.data, 
            context={'movie': self.movie, "request": self.request})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        data = CommentModelSerializer(comment).data
        return Response(data, status=status.HTTP_201_CREATED)
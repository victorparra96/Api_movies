"""Like views"""

# Django Rest Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from movies.models.comments import Comment
from movies.models.like import Like

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from movies.serializers.like import LikeModelSerializer, AddLikeSerializer


class LikeViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Like view set"""

    serializer_class = LikeModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the comment exists"""
        pk = kwargs['slug_name']
        self.comment = get_object_or_404(Comment, pk=pk)
        return super(LikeViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Like.objects.filter(is_active=True, comment=self.comment)
        return queryset

    def perform_destroy(self, instance):
        """Disable like"""
        instance.is_active = False
        # Dislike
        self.comment.comment_like = self.comment.comment_like - 1
        self.comment.save()
        instance.save()

    def create(self, request, *args, **kwargs):
        serializer = AddLikeSerializer(
            data=request.data, 
            context={'comment': self.comment, "request": self.request})
        serializer.is_valid(raise_exception=True)
        like = serializer.save()
        data = LikeModelSerializer(like).data
        return Response(data, status=status.HTTP_201_CREATED)
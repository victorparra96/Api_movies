# Django REST Framework
from rest_framework import serializers

# Model
from movies.models.like import Like


class LikeModelSerializer(serializers.ModelSerializer):
    """Like Model Serializer"""

    class Meta:
        """Meta class."""

        model = Like
        fields = (
            '__all__'
        )

class AddLikeSerializer(serializers.Serializer):
    """
    Add like serializer.
    Handle the addition of a new like to a comment.
    Comment object must be provided in the context
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        """Validate if the user added a like"""

        user = data['user']
        comment = self.context['comment']
        query = Like.objects.filter(user=user, comment=comment, is_active=True)
        if query.exists():
            raise serializers.ValidationError(f'User is already added like to comment')
        return data

    def create(self, data):
        """
        Crate a new like and update calculate
        field comment_like in comment.
        """

        user = data['user']
        comment = self.context['comment']

        comment_like, created = Like.objects.update_or_create(
            user=user,
            comment=comment,
            is_active=False,
            defaults={'is_active': 'True'}
        )

        # Update comment in column comment_like
        count_like = Like.objects.filter(is_active=True).count()
        comment.comment_like = count_like
        comment.save()

        return comment_like
    
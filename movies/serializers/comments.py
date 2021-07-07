# Django REST Framework
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

# Model
from movies.models.comments import Comment


class CommentReplyModelSerializer(serializers.ModelSerializer):
    """"Comments reply model serializers"""

    user = serializers.StringRelatedField()
    movie = serializers.StringRelatedField()

    class Meta:
        """Meta class."""

        model = Comment
        fields = (
            '__all__'
        )



class CommentModelSerializer(serializers.ModelSerializer):
    """Comments model serializers"""

    user = serializers.StringRelatedField()
    movie = serializers.StringRelatedField()
    replies = CommentReplyModelSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Comment
        exclude = ('reply',)


class AddCommentSerializer(serializers.Serializer):
    """
    Add comment serializer.
    Handle the addition of a new comment to a movie.
    Movie object must be provided in the context
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField(max_length=200)
    comment = serializers.IntegerField(default=0)

    def create(self, data):
        """Crate a new Comment"""

        user = data['user']
        movie = self.context['movie']
        comment_result = data['comment']
        comment_object = None

        # Get a comment instance
        if comment_result > 0:
            try:
                comment_object = get_object_or_404(Comment, pk=comment_result)
                print(comment_object)
            except:
                raise serializers.ValidationError("don't exists one comment for this id")

        # Create a new comment or reply for a comment
        comment = Comment.objects.create(
            user=user,
            movie=movie,
            description=data['description'],
            reply=comment_object
        )
        
        return comment

        

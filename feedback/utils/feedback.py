from rest_framework.response import Response

from feedback.api.serializers import ReactionSerializer, CommentSerializer
from feedback.models import Reaction, Comment
from response.rest import OkResponse


def get_all_reactions_of_a_news(news):
    reactions = Reaction.objects.filter(news=news)
    serializer = ReactionSerializer(reactions, many=True)

    # Return the serialized data as JSON response
    return Response({'reactions': serializer.data})


def get_all_comments_of_a_news(news):
    comments = Comment.objects.filter(news=news)
    serializer = CommentSerializer(comments, many=True)

    # Return the serialized data as JSON response
    return Response({'comments': serializer.data})

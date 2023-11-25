from rest_framework import serializers

from feedback.models import Reaction, Comment
from news.api.serializers import SubscriberSerializer, UserSerializer


class ReactionSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer()
    class Meta:
        model = Reaction
        fields = ('reactionType', 'created_time', 'subscriber')


class CommentSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer()
    class Meta:
        model = Comment
        fields = ['text', 'created_time', 'subscriber']

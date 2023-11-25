from rest_framework import serializers

from feedback.models import Reaction


class ReactionSerializer:
    class Meta:
        model = Reaction
        fields = ('reaction','created_time','subscriber')





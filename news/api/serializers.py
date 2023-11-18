from django.contrib.auth import get_user_model
from rest_framework import serializers

from news.models import Category, News, Like, DisLike, Comment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'username',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class AgencySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class LikeSerializer(serializers.ModelSerializer):
    # news = NewsSerializer()
    # user = UserSerializer()

    class Meta:
        model = Like
        fields = '__all__'


class DisLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DisLike
        fields = ('news', 'user')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('parent', 'news', 'user', 'description')


class NewsSerializer(serializers.ModelSerializer):
    agency = AgencySerializer()
    categories = CategorySerializer(many=True, read_only=True)
    # todo add like, dislike, comments
    likes = LikeSerializer(many=True, read_only=True)
    # todo fix this (not showing likes)

    class Meta:
        model = News
        fields = ('id', 'title', 'agency', 'description', 'icon', 'image', 'created_time', 'categories', 'likes')

from django.contrib.auth import get_user_model
from rest_framework import serializers

from news.models import Category, News


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


class NewsSerializer(serializers.ModelSerializer):
    agency = AgencySerializer()
    categories = CategorySerializer(many=True, read_only=True)
    #likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('token', 'title', 'agency', 'description', 'image', 'created_time', 'categories')

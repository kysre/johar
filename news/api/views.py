from django.http import HttpResponse

from rest_framework.decorators import (
    APIView,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from news.services.news import (
    login_by_username_password,
)
from response.rest import (
    OkResponse,
    NotFoundResponse,
    CreateUserSuccessResponse,
    CreateUserErrorResponse,
    LoginSuccessResponse,
    LoginErrorResponse,
)

from news.models import Subscriber, Agency, Category, News, Like, DisLike, Comment
from news.api.serializers import (UserSerializer, CategorySerializer,
                                  NewsSerializer, LikeSerializer, DisLikeSerializer,
                                  CommentSerializer)


def index(request):
    return HttpResponse("Hello, world. You're at the news index.")


@api_view(['POST'])
def user_signup(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        Subscriber.objects.create(user=user)
        return CreateUserSuccessResponse('User created successfully')
    else:
        errors = user_serializer.errors
        return CreateUserErrorResponse('Error creating user', errors)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    is_successful, message = login_by_username_password(username, password)
    if is_successful:
        token_key = message
        return LoginSuccessResponse(username, token_key)
    else:
        return LoginErrorResponse(message)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sample_api(request):
    # TODO: Do stuff
    return None


# Get news by Category title
class CategoryDetailView(APIView):
    def get(self, request, category_name):
        try:
            news = News.objects.filter(categories__title__contains=category_name)
            if news.exists():
                serializer = NewsSerializer(news, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail": "Category doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        except Category.DoesNotExist:
            return Response({"detail": "There is no News"}, status=status.HTTP_404_NOT_FOUND)


# Get all news
class AllNewsDetailView(APIView):
    def get(self, request):
        news = News.objects.all()
        if news.exists():
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "unknown Error"}, status=status.HTTP_400_BAD_REQUEST)

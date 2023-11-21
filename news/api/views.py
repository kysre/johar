from django.http import HttpResponse

from rest_framework.decorators import (
    APIView,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from news.services.news import (
    login_by_username_password,
)
from news.utils.news import (get_category_detail, get_landing_page_news, news_detail)
from response.rest import (
    OkResponse,
    NotFoundResponse,
    CreateUserSuccessResponse,
    CreateUserErrorResponse,
    LoginSuccessResponse,
    LoginErrorResponse
)

from news.models import Subscriber, Agency, Category, News
from news.api.serializers import (UserSerializer, CategorySerializer,
                                  NewsSerializer)


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
            news = get_category_detail(category_name)
        except News.DoesNotExist:
            return NotFoundResponse
        serializer = NewsSerializer(news, many=True)
        return OkResponse(news=serializer.data)


# Get all news
class LandingPageView(APIView):
    def get(self, request):
        try:
            news = get_landing_page_news()
        except News.DoesNotExist:
            return NotFoundResponse()
        serializer = NewsSerializer(news, many=True)
        return OkResponse(news=serializer.data)


class NewsDetailView(APIView):
    def get(self, request, token):
        try:
            news = news_detail(token)
        except News.DoesNotExist:
            return NotFoundResponse()
        serializer = NewsSerializer(news)
        return OkResponse(news=serializer.data)


class InsertNews(APIView):
    def post(self, request):
        pass

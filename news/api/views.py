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
    get_category_detail_service,
    get_landing_page_news_service,
    get_detail_view_service,
)
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
        is_successful, message = get_category_detail_service(category_name)
        if is_successful:
            serializer = NewsSerializer(message, many=True)
            return OkResponse(news=serializer.data)
        else:
            return NotFoundResponse(message=message)


# Get all news
class LandingPageView(APIView):
    def get(self, request):
        is_successful, message = get_landing_page_news_service()
        if is_successful:
            serializer = NewsSerializer(message, many=True)
            return OkResponse(news=serializer.data)
        else:
            return NotFoundResponse(message=message)


class NewsDetailView(APIView):
    def get(self, request, token):
        is_successful, message = get_detail_view_service(token)
        if is_successful:
            serializer = NewsSerializer(message)
            return OkResponse(news=serializer.data)
        else:
            return NotFoundResponse(message=message)


class AddNews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # check user auth

        # check is it reporter

        # add news
        pass

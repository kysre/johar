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
    is_user_reporter,
    is_reporter_author,
    create_news_service,
    update_news_service,
    delete_news,
    search_for_news,
)
from response.rest import (
    OkResponse,
    NotFoundResponse,
    CreateUserSuccessResponse,
    CreateUserErrorResponse,
    LoginSuccessResponse,
    LoginErrorResponse,
    AccessErrorResponse,
    BadRequestResponse,
)

from news.models import Subscriber
from news.api.serializers import (UserSerializer, CategorySerializer,
                                  NewsSerializer, ReporterSerializer, AgencySerializer)


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


class NewsSearchView(APIView):
    def get(self, request, keyword):
        is_successful, message = search_for_news(keyword)
        if is_successful:
            serializer = NewsSerializer(message, many=True)
            return OkResponse(news=serializer.data)
        else:
            return NotFoundResponse(message=message)


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
            return OkResponse(news=message)
        else:
            return NotFoundResponse(message=message)


class NewsDetailView(APIView):
    def get(self, request, token):
        is_successful, message = get_detail_view_service(token)
        if is_successful:
            return OkResponse(news=message)
        else:
            return NotFoundResponse(message=message)


class AddNews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # check is it reporter
        username = request.user.username
        is_successful, reporter = is_user_reporter(username)

        if not is_successful:
            return AccessErrorResponse('user cant add news(not a reporter)')

        # add news
        is_successful, message = create_news_service(request.data, reporter)
        if is_successful:
            return OkResponse(message=message)
        else:
            return BadRequestResponse(message)


class UpdateNewsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, token):
        # check is it reporter
        username = request.user.username
        is_successful, reporter = is_user_reporter(username)
        if not is_successful:
            return AccessErrorResponse('user cant update news(not a reporter)')

        # check if reporter is author of news
        is_successful, message = is_reporter_author(reporter, token)
        if not is_successful:
            return BadRequestResponse(message)

        news = message
        # update news
        is_successful, message = update_news_service(request.data, news)
        if is_successful:
            return OkResponse(message=message)
        else:
            return BadRequestResponse(message)


class DeleteNewsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, token):
        # check is it reporter
        username = request.user.username
        is_successful, reporter = is_user_reporter(username)
        if not is_successful:
            return AccessErrorResponse('user cant update news(not a reporter)')

        # check if reporter is author of news
        is_successful, message = is_reporter_author(reporter, token)
        if not is_successful:
            return BadRequestResponse(message)

        news = message

        # delete
        is_successful, message = delete_news(news)
        if is_successful:
            return OkResponse(message=message)
        else:
            return BadRequestResponse(message)

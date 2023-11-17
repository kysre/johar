from django.http import HttpResponse

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from news.models import Subscriber
from news.api.serializers import (
    UserSerializer,
)
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

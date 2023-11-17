from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


def is_authentication_successful(username: str, password: str) -> bool:
    user = authenticate(username=username, password=password)
    return user is not None


def get_user_token_key(username: str, password: str) -> str:
    user = authenticate(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return token.key

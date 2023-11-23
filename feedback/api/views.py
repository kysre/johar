from django.http import HttpResponse

from rest_framework.decorators import (
    APIView,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from feedback.models import Reaction,Comment
from news.models import News, Subscriber
from news.utils.authentication import get_user_By_token

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


class ReactToNews(APIView):
    def post(self, request, pk):
        try:
            news = News.objects.get(token=pk)
            react = request.data.get('reaction')
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
            user = get_user_By_token(token_key=token)
            subscriber = Subscriber.objects.get(user=user)
            reaction = Reaction(subscriber=subscriber, news=news, reaction=Reaction.convert_str_to_reaction_type(react))
            reaction.save()
            return OkResponse()
        except News.DoesNotExist:
            return NotFoundResponse()


class CommentOnNews(APIView):
    def post(self, request, pk):
        try:
            news = News.objects.get(token=pk)
            text = request.data.get('comment')
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
            user = get_user_By_token(token_key=token)
            username = user.username
            comment = Comment(username=username, news=news, text=text)
            comment.save()
            return OkResponse()
        except News.DoesNotExist:
            return NotFoundResponse()
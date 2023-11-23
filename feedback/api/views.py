from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import (
    APIView,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from feedback.models import Reaction, Comment
from news.models import News, Subscriber
from news.utils.authentication import get_user_By_token

from response.rest import (
    OkResponse,
    NotFoundResponse,
    CreateUserSuccessResponse,
    CreateUserErrorResponse,
    LoginSuccessResponse,
    LoginErrorResponse,
    NotAuthorizedResponse,
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
            if user is None:
                return NotAuthorizedResponse('Your access token is invalid')
            subscriber = Subscriber.objects.get(user=user)
            reaction = Reaction(subscriber=subscriber, news=news, reaction=Reaction.convert_str_to_reaction_type(react))
            reaction.save()
            return OkResponse()
        except News.DoesNotExist:
            return NotFoundResponse()

    def get(self, request, pk):
        try:
            news = News.objects.get(token=pk)
            reactions_for_news = Reaction.objects.filter(news=news)
            reactions_list = [{'username': reaction.subscriber.user.username, 'created_time': reaction.created_time,
                               'reaction': reaction.reaction}
                              for reaction in reactions_for_news]

            return JsonResponse({'reactions': reactions_list})
        except News.DoesNotExist:
            return NotFoundResponse()


class CommentOnNews(APIView):
    def post(self, request, pk):
        try:
            news = News.objects.get(token=pk)
            text = request.data.get('comment')
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
            user = get_user_By_token(token_key=token)
            if user is None:
                return NotAuthorizedResponse('Your access token is invalid')
            username = user.username
            comment = Comment(username=username, news=news, text=text)
            comment.save()
            return OkResponse()
        except News.DoesNotExist:
            return NotFoundResponse()

    def get(self, request, pk):
        try:
            news = News.objects.get(token=pk)
            comments_for_news = Comment.objects.filter(news=news)
            comments_list = [{'username': comment.username, 'created_time': comment.created_time, 'text': comment.text}
                             for comment in comments_for_news]

            return JsonResponse({'comments': comments_list})
        except News.DoesNotExist:
            return NotFoundResponse()

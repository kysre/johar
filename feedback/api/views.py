from rest_framework.decorators import (
    APIView,
)
from feedback.services.feedback import create_reaction_service, create_comment_service
from feedback.utils.feedback import get_all_reactions_of_a_news, get_all_comments_of_a_news
from news.models import News, Subscriber
from news.utils.news import news_detail

from response.rest import (
    NotFoundResponse,
)


class ReactToNews(APIView):
    def post(self, request, token):
        try:
            news = news_detail(token=token)
            # add reaction
            response = create_reaction_service(request, news)
            return response
        except News.DoesNotExist:
            return NotFoundResponse()
    def get(self, request, token):
        try:
            news = news_detail(token=token)
            # add reaction
            response = get_all_reactions_of_a_news(news)
            return response
        except News.DoesNotExist:
            return NotFoundResponse()


class CommentOnNews(APIView):
    def post(self, request, token):
        try:
            news = news_detail(token=token)
            # add comment
            response = create_comment_service(request, news)
            return response
        except News.DoesNotExist:
            return NotFoundResponse()

    def get(self, request, token):
        try:
            news = news_detail(token=token)
            # add reaction
            response = get_all_comments_of_a_news(news)
            return response
        except News.DoesNotExist:
            return NotFoundResponse()

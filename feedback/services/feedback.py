from feedback.models import Reaction, Comment
from news.models import Subscriber
from news.utils.authentication import get_user_by_token
from response.rest import (
    OkResponse,
    NotAuthorizedResponse,
)


def create_reaction_service(request, news):
    react = request.data.get('reaction')
    _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
    user = get_user_by_token(token_key=token)
    if user is None:
        return NotAuthorizedResponse('Your access token is invalid')
    subscriber = Subscriber.objects.get(user=user)
    reaction = Reaction(subscriber=subscriber, news=news, reaction=Reaction.convert_str_to_reaction_type(react))
    reaction.save()
    return OkResponse()


def create_comment_service(request, news):
    text = request.data.get('comment')
    _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
    user = get_user_by_token(token_key=token)
    if user is None:
        return NotAuthorizedResponse('Your access token is invalid')
    subscriber = Subscriber.objects.get(user=user)
    comment = Comment(subscriber=subscriber, news=news, text=text)
    comment.save()
    return OkResponse()

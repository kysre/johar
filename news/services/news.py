from typing import Tuple

from news.utils.news import (get_category_detail, get_landing_page_news, news_detail)
from news.models import Subscriber, Agency, Category, News


def login_by_username_password(username: str, password: str) -> Tuple[bool, str]:
    from news.utils.authentication import is_authentication_successful
    from news.utils.authentication import get_user_token_key

    if not is_authentication_successful(username, password):
        return False, 'Invalid login credentials'
    else:
        token_key = get_user_token_key(username, password)
        return True, token_key


def get_category_detail_service(category_name):
    try:
        news = get_category_detail(category_name)
        if len(news):
            return True, news
        else:
            return False, 'Invalid Category name'
    except News.DoesNotExist:
        return False, 'Invalid Category name'


def get_landing_page_news_service():
    try:
        news = get_landing_page_news()
        return True, news
    except News.DoesNotExist:
        return False, 'No news in last 7 days'


def get_detail_view_service(token):
    try:
        news = news_detail(token)
        return True, news
    except News.DoesNotExist:
        return False, 'there is no post with this token'

from typing import Tuple
import random

from news.utils.news import (get_category_detail, get_landing_page_news, news_detail, get_reporter, get_category_id)
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


def is_user_reporter(username):
    reporter = get_reporter(username)
    if reporter is None:
        return False, 'User is not reporter'
    else:
        return True, reporter


def creat_news_service(data, reporter):
    if 'title' not in data:
        return False, 'news should have title'
    if 'description' not in data:
        return False, 'news should have description'
    categories = [get_category_id(category_name) for category_name in data.get('categories')]
    token = creat_unique_token()
    data.pop('categories')
    news = News(**data, token=token, author=reporter, agency=reporter.agency)
    news.save()
    news.categories.set(categories)
    return True, 'news created successfully'


def creat_unique_token():
    while True:
        random_token = random.randint(10 ** 11, 10 ** 12 - 1)
        try:
            news = news_detail(random_token)
        except News.DoesNotExist:
            return random_token


from typing import Tuple
import os
import base64
import time
import struct

from news.utils.news import (
    get_category_detail,
    get_landing_page_news,
    get_news_by_token,
    get_reporter,
    get_category_id,
    get_news_by_title_detail,
    get_news_by_description_detail,
)
from news.utils.news_cache import NewsCache
from news.models import News
from news.api.serializers import NewsSerializer


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
    resp = NewsCache.get_news_landing_page()
    if resp is None:
        try:
            news = get_landing_page_news()
        except News.DoesNotExist:
            return False, 'No news in last 7 days'
        resp = NewsSerializer(news, many=True).data
        NewsCache.set_news_landing_page(resp)
    return True, resp


def get_detail_view_service(token: str):
    resp = NewsCache.get_news_data(token)
    if resp is None:
        try:
            news = get_news_by_token(token)
        except News.DoesNotExist:
            return False, 'there is no post with this token'
        resp = NewsSerializer(news).data
        NewsCache.set_news_data(token, resp)
    return True, resp


def is_user_reporter(username):
    reporter = get_reporter(username)
    if reporter is None:
        return False, 'User is not reporter'
    else:
        return True, reporter


def is_reporter_author(reporter, token):
    try:
        news = get_news_by_token(token)
    except News.DoesNotExist:
        return False, 'news does not exists'
    news_author = news.author
    if news_author == reporter:
        return True, news
    return False, 'reporter is not author of news'


def search_for_news(keyword):
    news_with_title_keyword = get_news_by_title_detail(keyword)
    news_with_description_keyword = get_news_by_description_detail(keyword)
    all_matched_news = list(news_with_title_keyword)
    all_matched_news.extend(list(news_with_description_keyword))
    if len(all_matched_news) == 0:
        return False, 'No news matched that keyword'
    else:
        return True, all_matched_news


def create_news_service(data, reporter):
    if 'title' not in data:
        return False, 'news should have title'
    if 'description' not in data:
        return False, 'news should have description'
    categories = [get_category_id(category_name) for category_name in data.get('categories')]
    token = create_unique_token()
    data.pop('categories')
    news = News(**data, token=token, author=reporter, agency=reporter.agency)
    news.categories.set(categories)
    news.save()
    return True, 'news created successfully'


def update_news_service(data, news):
    # check data to be valid
    editable_fields = ['title', 'description', 'is_draft', 'categories']
    if not all(key in editable_fields for key in data):
        return False, 'bad data format'

    # update categories
    if 'categories' in data.keys():
        categories = [get_category_id(category_name) for category_name in data.get('categories')]
        data.pop('categories')
        news.categories.set(categories)
    # update other fields
    for field, value in data.items():
        # check field can be updated
        setattr(news, field, value)
    news.save()

    # save changes into cache
    resp = NewsSerializer(news).data
    NewsCache.set_news_data(news.token, resp)
    return True, 'news updated successfully'


def delete_news(news):
    news.delete()

    # todo delete from cache
    return True, 'news deleted successfully'


def generate_random_urlsafe(length):
    # generate random part
    CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    return "".join([CHARSET[c & 63] for c in os.urandom(length)])


def generate_token():
    time_part = base64.urlsafe_b64encode(
        struct.pack('I', int(time.time()))
    )[5::-1]
    return time_part.decode("utf-8") + generate_random_urlsafe(6)


def create_unique_token():
    while True:
        random_token = generate_token()
        try:
            news = get_news_by_token(random_token)
        except News.DoesNotExist:
            return random_token

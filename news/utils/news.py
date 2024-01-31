import os
import random

from django.contrib.auth import get_user_model
from django.db.models import Max

from news.models import News, Category, Reporter, Agency
from datetime import datetime, timedelta


def get_category_detail(category_name):
    news = News.objects.filter(categories__title__contains=category_name)
    return news


def get_landing_page_news():
    seven_days_ago = datetime.now() - timedelta(days=7)
    news = News.objects.filter(created_time__range=(seven_days_ago, datetime.now()))
    return news


def get_news_by_token(token):
    return News.objects.get(token=token)


def get_reporter_by_username(username):
    try:
        subscriber = get_user_model().objects.get(username=username).subscriber
        reporter = Reporter.objects.get(subscriber=subscriber)
        return reporter
    except (get_user_model().DoesNotExist, Reporter.DoesNotExist):
        return None


def get_subscriber_by_username(username):
    try:
        subscriber = get_user_model().objects.get(username=username).subscriber
        return subscriber
    except get_user_model().DoesNotExist:
        return None


def get_agency_by_name(name):
    try:
        agency = Agency.objects.get(name=name)
        return agency
    except Agency.DoesNotExist:
        return None


def get_category_id(category_name):
    category = Category.objects.get(title=category_name)
    return category.id


def get_news_by_title_detail(keyword: str):
    return News.objects.filter(title__icontains=keyword)


def get_news_by_description_detail(keyword: str):
    return News.objects.filter(description__icontains=keyword)


def get_random_news(excluded_tokens=None):
    if excluded_tokens is None:
        excluded_tokens = []
    suggestion_count = int(os.environ.get('NEWS_SUGGESTION_COUNT', 5))
    query_set = News.objects.exclude(token__in=excluded_tokens)
    return get_random_obj_from_queryset(query_set, suggestion_count)


def get_random_obj_from_queryset(queryset, count=1):
    max_pk = queryset.aggregate(max_pk=Max("pk"))['max_pk']
    random_pks = [random.randint(1, max_pk) for _ in range(count)]
    while True:
        objs = queryset.filter(pk__in=random_pks).all()
        return objs

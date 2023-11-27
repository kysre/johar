from django.contrib.auth import get_user_model

from news.models import News, Category, Reporter, Subscriber, Agency
from datetime import datetime, timedelta
from news.utils.news_cache import NewsCache


def get_category_detail(category_name):
    news = News.objects.filter(categories__title__contains=category_name)
    return news


def get_landing_page_news():
    seven_days_ago = datetime.now() - timedelta(days=7)
    news = News.objects.filter(created_time__range=(seven_days_ago, datetime.now()))
    return news


def get_news_by_token(token):
    return News.objects.get(token=token)


def get_reporter(username):
    try:
        subscriber = get_user_model().objects.get(username=username).subscriber
        reporter = Reporter.objects.get(subscriber=subscriber)
        return reporter
    except (get_user_model().DoesNotExist, Reporter.DoesNotExist):
        return None


def get_subscriber(username):
    try:
        subscriber = get_user_model().objects.get(username=username).subscriber
        return subscriber
    except get_user_model().DoesNotExist:
        return None


def get_agency(name):
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

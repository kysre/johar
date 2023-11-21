from news.models import News, Category
from datetime import datetime, timedelta


def get_category_detail(category_name):
    news = News.objects.filter(categories__title__contains=category_name)
    return news


def get_landing_page_news():
    seven_days_ago = datetime.now() - timedelta(days=7)
    news = News.objects.filter(created_time__range=(seven_days_ago, datetime.now()))
    return news


def news_detail(token):
    news = News.objects.get(token=token)
    return news


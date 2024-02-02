from typing import List, Any
import random
import string
import os
from faker import Faker

from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from news.models import (
    Subscriber,
    Reporter,
    Agency,
    Category,
    News,
    Subscription,
)
from news.services.news import create_unique_token


def get_random_obj(objects: List[Any]) -> Any:
    random_index = random.randint(0, len(objects) - 1)
    return objects[random_index]


def generate_fake_data():
    SUBSCRIBER_COUNT = int(os.getenv("SUBSCRIBER_COUNT", 100))
    AGENCY_COUNT = int(os.getenv("AGENCY_COUNT", 10))
    REPORTER_PER_AGENCY = int(os.getenv("REPORTER_PER_AGENCY", 2))
    NEWS_COUNT = int(os.getenv("NEWS_COUNT", 1000))
    MAX_SUBSCRIPTION_COUNT = int(os.getenv("MAX_SUBSCRIPTION_COUNT", 3))

    fake = Faker()
    # Create subscribers
    subscribers = []
    for i in range(SUBSCRIBER_COUNT):
        username = fake.user_name()
        email = f"{username}@example.com"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user = get_user_model().objects.create_user(username=username, email=email, password=password)
        subscriber = Subscriber.objects.create(user=user)
        subscribers.append(subscriber)

    reporters = []
    agencies = []
    for i in range(AGENCY_COUNT):
        agency = Agency.objects.create(name=fake.company(), description=fake.paragraph())
        agencies.append(agency)
        for j in range(REPORTER_PER_AGENCY):
            subscriber = subscribers[i * REPORTER_PER_AGENCY + j]
            reporter = Reporter.objects.create(
                subscriber=subscriber,
                avatar=None,
                agency=agency,
                about_me=fake.paragraph(),
            )
            reporters.append(reporter)

    for subscriber in subscribers:
        for i in range(MAX_SUBSCRIPTION_COUNT):
            should_subscribe = True if random.randint(0, 1) == 1 else False
            if should_subscribe:
                agency = get_random_obj(agencies)
                Subscription.objects.create(subscriber=subscriber, agency=agency)

    categories = [Category.objects.create(title='Sports', description=fake.text()),
                  Category.objects.create(title='Weather', description=fake.text()),
                  Category.objects.create(title='Travel', description=fake.text()),
                  Category.objects.create(title='International', description=fake.text()),
                  Category.objects.create(title='Politics', description=fake.text()),
                  Category.objects.create(title='Economics', description=fake.text())]

    for i in range(NEWS_COUNT):
        reporter = get_random_obj(reporters)
        news = News.objects.create(
            title=fake.sentence(),
            agency=reporter.agency,
            author=reporter,
            token=create_unique_token(),
            image=None,
            description=fake.text(),
            is_draft=fake.boolean(),
        )
        news_categories = []
        if fake.boolean():
            news_categories.append(get_random_obj(categories))
            if fake.boolean():
                news_categories.append(get_random_obj(categories))
        news.categories.set(news_categories)


class Command(BaseCommand):
    help = 'Generate some fake data for testing'

    def handle(self, *args, **options):
        generate_fake_data()

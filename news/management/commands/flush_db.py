from typing import List, Any
import random

from django.core.management import BaseCommand
from django.db.models import Q
from django.contrib.auth import get_user_model

from news.models import (
    Subscriber,
    Reporter,
    Agency,
    Category,
    News,
)


def get_random_obj(objects: List[Any]) -> Any:
    random_index = random.randint(0, len(objects) - 1)
    return objects[random_index]


def generate_fake_data():
    News.objects.all().delete()
    Category.objects.all().delete()
    Reporter.objects.all().delete()
    Agency.objects.all().delete()
    Subscriber.objects.all().delete()
    get_user_model().objects.all().filter(~Q(username='admin')).delete()


class Command(BaseCommand):
    help = 'Delete all data from db'

    def handle(self, *args, **options):
        generate_fake_data()

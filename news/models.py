from django.contrib.auth import get_user_model
from django.db import models


class Subscriber(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Reporter(models.Model):
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, default=None, upload_to='reporters')
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE)
    about_me = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subscriber.user.username


class Agency(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    image = models.ImageField(blank=True, default=None, upload_to='agencies')

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250)
    icon = models.ImageField(blank=True, default=None, upload_to='categories')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=250)
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE)
    author = models.ForeignKey('Reporter', on_delete=models.PROTECT)
    token = models.CharField(max_length=12, unique=True)
    image = models.ImageField(blank=True, null=True, default=None, upload_to='news')
    description = models.TextField()
    is_draft = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True, default=None)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.id) + str(self.agency)} + {self.title}'

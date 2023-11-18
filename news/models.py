from django.contrib.auth import get_user_model
from django.db import models


class Subscriber(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Agency(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    # todo add other fields

    def __str__(self):
        return self.user.username


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250)
    icon = models.ImageField(blank=True, upload_to='categories')
    is_enable = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=50)
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news')
    description = models.TextField()
    icon = models.ImageField(blank=True, upload_to='categories')
    is_enable = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.agency)} + {self.title}'


class Like(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('Subscriber', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class DisLike(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('Subscriber', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    user = models.ForeignKey('Subscriber', on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    is_enable = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    # todo add update?

    def __str__(self):
        return f'{str(self.news)} + {str(self.user)}'

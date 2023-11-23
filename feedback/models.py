from django.db import models

# Create your models here.
from news.models import News, Subscriber


class Reaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('subscriber', 'news')

    def __str__(self):
        return f'{str(self.news) + str(self.subscriber)} + {self.reaction}'

    @staticmethod
    def convert_str_to_reaction_type(inputString):
        if inputString.lower() == "like":
            return Reaction.LIKE
        elif inputString.lower() == "dislike":
            return Reaction.DISLIKE
        else:
            return None


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    text = models.CharField(max_length=150)

    def __str__(self):
        return f"Comment by {self.username} on {self.news}"

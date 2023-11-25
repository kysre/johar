from django.urls import path

from feedback.api import views

urlpatterns = [
    path('<str:token>/reaction', views.ReactToNews.as_view()),
    path('<str:token>/comment', views.CommentOnNews.as_view()),
]

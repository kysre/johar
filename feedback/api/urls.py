from django.urls import path

from feedback.api import views

urlpatterns = [
    path('<int:pk>/reaction', views.ReactToNews.as_view()),
    path('<int:pk>/comment', views.CommentOnNews.as_view()),
]

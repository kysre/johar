from django.urls import path

from news.api import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/', views.user_signup),
    path('login/', views.login),
]

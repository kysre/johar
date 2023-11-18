from django.urls import path

from news.api import views

urlpatterns = [
    path('', views.AllNewsDetailView.as_view(), name='index'),
    path('sign_up/', views.user_signup),
    path('login/', views.login),
    path('categories/<str:category_name>/', views.CategoryDetailView.as_view(), name='category_name'),
]

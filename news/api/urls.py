from django.urls import path

from news.api import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='index'),
    path('<int:token>/', views.NewsDetailView.as_view()),
    path('sign_up/', views.user_signup),
    path('login/', views.login),
    path('categories/<str:category_name>/', views.CategoryDetailView.as_view(), name='category_name'),
    path('add/', views.AddNews.as_view()),
    path('update/<int:token>', views.UpdateNewsView.as_view()),
    path('search/<str:keyword>', views.NewsSearchView.as_view()),
]

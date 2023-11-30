from django.urls import path

from news.api import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='index'),
    path('sign_up/', views.user_signup),
    path('login/', views.login),
    path('categories/<str:category_name>/', views.CategoryDetailView.as_view(), name='category_name'),
    path('add/', views.AddNews.as_view()),
    path('update/<str:token>', views.UpdateNewsView.as_view()),
    path('delete/<str:token>', views.DeleteNewsView.as_view()),
    path('create_agency', views.CreateAgencyView.as_view()),
    path('add_reporter', views.AddReporterView.as_view()),
    path('search/<str:keyword>', views.NewsSearchView.as_view()),
    path('<str:token>/', views.NewsDetailView.as_view()),
]

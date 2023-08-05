from django.urls import path
from . import views


app_name = 'news'


urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<str:category_slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('most-viewed/', views.MostViewedPosts.as_view(), name='most-viewed'),
    path('last-week/', views.LastWeek.as_view(), name='last-week'),
    path('ads/', views.AddAPIView.as_view(), name='adds'),
    path('weather/', views.WeatherAPIView.as_view(), name='weather'),
    path('social/', views.SocialAccountsAPIView.as_view(), name='social-accounts'),
    path('footer-data/', views.FooterDataAPIView.as_view(), name='footer-data'),
    path('currency/', views.Currency.as_view(), name='currency'),
    path('search/', views.PostSearchAPIView.as_view(), name='post_search'),
    path('', views.PostListAPIView.as_view(), name='post-list'),
]
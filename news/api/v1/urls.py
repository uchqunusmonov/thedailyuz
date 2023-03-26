from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<str:category_slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('most-viewed/', views.MostViewedPosts.as_view(), name='most-viewed'),
    path('last-week/', views.LastWeek.as_view(), name='last-week'),
    path('adds/', views.AddAPIView.as_view(), name='adds'),
    path('', views.PostListAPIView.as_view(), name='post-list'),
]
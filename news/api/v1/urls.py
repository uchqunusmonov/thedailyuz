from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<str:category_slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
]
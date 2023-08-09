from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status
from news.api.v1.serializers import CategorySerializer, PostSerializer, AddSerializer, WeatherSerializer, SocialAccountsSerializer, FooterDataSerializer
from ...models import Category, Post, Add, Weather, SocialAccounts, FooterData
from rest_framework import views
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.utils import timezone
import requests
from django.db.models import Q
from news.pagination import Pagination
from rest_framework import generics


class CategoryListView(views.APIView):
    """
    List all categories
    """

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetailView(views.APIView):
    """
    List posts by category
    """
    pagination_class = Pagination()

    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category)
        paginator = self.pagination_class
        result_page = paginator.paginate_queryset(queryset=posts, request=request, view=self)
        serializer = PostSerializer(result_page, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response.data, status=status.HTTP_200_OK)


class PostListAPIView(generics.ListAPIView):
    """
    List and Retrieve all posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = Pagination


class PostDetailAPIView(views.APIView):
    """
    Post detail view
    """
    pagination_class = Pagination()

    def get(self, request, year, month, day, slug):
        try:
            post = Post.objects.select_related('category').get(
                slug=slug,
                created__year=year,
                created__month=month,
                created__day=day
            )
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status.HTTP_404_NOT_FOUND)

        # update views count
        post.views_count += 1
        post.save(update_fields=['views_count'])

        # get posts
        serializer = PostSerializer(post)

        # Get similar posts based on the post's category and add pagination
        similar_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:8]
        paginator = self.pagination_class
        result_page = paginator.paginate_queryset(similar_posts, request)
        similar_posts_serializer = PostSerializer(result_page, many=True)

        # add the similar posts to the serialized data
        data = {
            'posts': serializer.data,
            'similar_posts': paginator.get_paginated_response(similar_posts_serializer.data).data
        }

        return Response(data, status.HTTP_200_OK)


class MostViewedPosts(views.APIView):

    def get(self, request):
        day = timezone.now() - timezone.timedelta(days=2)
        posts = Post.objects.annotate(total_views=Count('views_count')).\
            filter(
            created__gte=day, views_count__gt=0
        ).order_by('-total_views')
        paginator = PageNumberPagination()
        paginator.page_size = 4
        rs_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(rs_page, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class LastWeek(views.APIView):

    def get(self, request):
        day = timezone.now() - timezone.timedelta(days=7)
        posts = Post.objects.filter(created__gte=day).order_by('created')
        paginator = PageNumberPagination()
        paginator.page_size = 4
        rs_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(rs_page, many=True)
        return Response(serializer.data)


class AddAPIView(views.APIView):
    """
    Get active Adds with pagination
    """
    def get(self, request):
        adds = Add.objects.filter(is_active=True)
        paginator = PageNumberPagination()
        paginator.page_size = 1
        rs_page = paginator.paginate_queryset(adds, request)
        serializer = AddSerializer(rs_page, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class WeatherAPIView(views.APIView):
    def get(self, request):
        location = request.query_params.get('location')
        if location is None:
            return Response({'error': 'Please provide a location query parameter'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            weather = Weather.objects.get(location=location)
        except Weather.DoesNotExist:
            return Response({'message': '404 Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WeatherSerializer(weather)
        return Response(serializer.data, status.HTTP_200_OK)


class SocialAccountsAPIView(views.APIView):
    def get(self, request):
        queryset = SocialAccounts.objects.all()
        serializer = SocialAccountsSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class FooterDataAPIView(views.APIView):

    def get(self, request):
        queryset = FooterData.objects.last()
        serializer = FooterDataSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class Currency(views.APIView):
    def get(self, request):
        url = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
        response = requests.request('GET', url)
        response_data = response.json()
        data = {
            'usd': {
                'name': response_data[0]['Ccy'],
                'rate': response_data[0]['Rate'],
                'diff': response_data[0]['Diff']
            },
            'eur': {
                'name': response_data[1]['Ccy'],
                'rate': response_data[1]['Rate'],
                'diff': response_data[1]['Diff']
            },
            'rub': {
                'name': response_data[2]['Ccy'],
                'rate': response_data[2]['Rate'],
                'diff': response_data[2]['Diff']
            }
        }
        return Response(data)


class PostSearchAPIView(views.APIView):
    """
    Search for posts
    """
    def get(self, request):
        query = request.GET.get('q')
        if not query:
            return Response({"error": "Search query parameter is missing"}, status.HTTP_400_BAD_REQUEST)

        queryset = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PostSerializer(result_page, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
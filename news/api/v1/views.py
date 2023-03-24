from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from news.api.v1.serializers import CategorySerializer, PostSerializer
from ...models import Category, Post
from rest_framework import views
from rest_framework.pagination import PageNumberPagination


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

    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category)
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status
from news.api.v1.serializers import CategorySerializer, PostSerializer, AddSerializer, WeatherSerializer, SocialAccountsSerializer, FooterDataSerializer, CategoryDetailSerializer
from ...models import Category, Post, Add, Weather, SocialAccounts, FooterData
from rest_framework import views
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.utils import timezone
import requests
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CategoryListView(views.APIView):
    """
    List all categories
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of categories',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                            'slug': openapi.Schema(type=openapi.TYPE_STRING),
                            'url': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                )
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description='Server error',
            ),
        }
    )
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
        serializer = CategoryDetailSerializer(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostListAPIView(views.APIView):
    """
    List and Retrieve all posts
    """

    swagger_auto_schema(
        operation_description="Get all posts paginated",
        responses={200: PostSerializer(many=True)},
        tags=["Posts"],
    )

    def get(self, request):
        queryset = Post.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PostSerializer(result_page, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class PostDetailAPIView(views.APIView):
    """
    Post detail view
    """

    @swagger_auto_schema(
        operation_description="Get post details",
        operation_summary="Retrieve a post by year, month, day and slug",
        responses={
            200: PostSerializer(),
            404: "Post not found"
        },
        tags=["Posts"],
        manual_parameters=[
            openapi.Parameter(
                name="year",
                in_=openapi.IN_PATH,
                description="Year of the post creation date",
                required=True,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="month",
                in_=openapi.IN_PATH,
                description="Month of the post creation date",
                required=True,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="day",
                in_=openapi.IN_PATH,
                description="Day of the post creation date",
                required=True,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="slug",
                in_=openapi.IN_PATH,
                description="Slug of the post",
                required=True,
                type=openapi.TYPE_STRING
            ),
        ]
    )
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
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(similar_posts, request)
        similar_posts_serializer = PostSerializer(result_page, many=True)

        # add the similar posts to the serialized data
        data = {
            'posts': serializer.data,
            'similar_posts': similar_posts_serializer.data
        }

        return Response(data, status.HTTP_200_OK)


class MostViewedPosts(views.APIView):
    @swagger_auto_schema(
        operation_description='Get a list of posts that have been viewed the most in the last 2 days.',
        responses={
            200: openapi.Response(
                description='OK',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                        'content': openapi.Schema(type=openapi.TYPE_STRING),
                        'created': openapi.Schema(type=openapi.TYPE_STRING),
                        'category': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'slug': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    }
                )
            )
        }
    )
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
    @swagger_auto_schema(
        operation_summary="List posts created in the last week",
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="The total number of posts returned.",
                        ),
                        "next": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="URL of the next page of results.",
                        ),
                        "previous": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="URL of the previous page of results.",
                        ),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="The post ID.",
                                    ),
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="The post title.",
                                    ),
                                    "slug": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="The post slug.",
                                    ),
                                    "body": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="The post body.",
                                    ),
                                    "pub_date": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        description="The publication date of the post.",
                                    ),
                                    "views_count": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="The number of views the post has received.",
                                    ),
                                    "category": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="The category ID.",
                                            ),
                                            "title": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="The category title.",
                                            ),
                                            "slug": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="The category slug.",
                                            ),
                                        },
                                        description="The category of the post.",
                                    ),
                                },
                                description="The post object.",
                            ),
                            description="The list of posts created in the last week.",
                        ),
                    },
                ),
            ),
        },
    )
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

    @swagger_auto_schema(
        operation_description="Get active Adds with pagination",
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'image': openapi.Schema(type=openapi.TYPE_STRING),
                        'created': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'updated': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                ),
            )
        }
    )
    def get(self, request):
        adds = Add.objects.filter(is_active=True)
        paginator = PageNumberPagination()
        paginator.page_size = 1
        rs_page = paginator.paginate_queryset(adds, request)
        serializer = AddSerializer(rs_page, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class WeatherAPIView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get weather data for a location",
        manual_parameters=[
            openapi.Parameter(
                name='location',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='The location to fetch weather data for',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='OK',
                schema=WeatherSerializer
            ),
            400: openapi.Response(
                description='Bad Request',
                examples={
                    'application/json': {
                        'error': 'Please provide a location query parameter'
                    }
                }
            ),
            404: openapi.Response(
                description='Not Found',
                examples={
                    'application/json': {
                        'message': '404 Not Found'
                    }
                }
            )
        }
    )
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
    @swagger_auto_schema(
        operation_description="Get all social accounts",
        responses={200: SocialAccountsSerializer(many=True)},
    )
    def get(self, request):
        queryset = SocialAccounts.objects.all()
        serializer = SocialAccountsSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class FooterDataAPIView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get the latest footer data",
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING)
                    },
                ),
            ),
            404: "Not Found",
        },
    )
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

from rest_framework import serializers
from news.models import Category, Post, Add, Weather, REGIONS, SocialAccounts, FooterData
from rest_framework.pagination import PageNumberPagination


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'url']

    def get_url(self, obj):
        return obj.get_absolute_url()


class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'body', 'created', 'updated', 'views_count', 'url']

    def get_url(self, obj):
        return obj.get_absolute_url()


class CategoryDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['title', 'url', 'posts']

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_posts(self, obj):
        posts = Post.objects.filter(category=obj)
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(posts, self.context['request'])
        return PostSerializer(result_page, many=True).data


class AddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add
        fields = ['id', 'image', 'url', 'click_count']


class WeatherSerializer(serializers.ModelSerializer):
    location = serializers.ChoiceField(choices=REGIONS, default='41.2995,69.2401')

    class Meta:
        model = Weather
        fields = ['id', 'location', 'temp', 'text', 'icon']


class SocialAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccounts
        fields = ['id', 'name', 'url']


class FooterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterData
        fields = ['id', 'phone_number', 'email']

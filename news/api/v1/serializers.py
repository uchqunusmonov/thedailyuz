from rest_framework import serializers
from news.models import Category, Post, Add, Weather, REGIONS, SocialAccounts, FooterData


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['id', 'category', 'image', 'title', 'body', 'created', 'updated', 'views_count']


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
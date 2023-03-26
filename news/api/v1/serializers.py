from rest_framework import serializers
from news.models import Category, Post, Add


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

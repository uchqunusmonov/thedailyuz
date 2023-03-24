from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'image', 'slug', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title', )}
    readonly_fields = ['views_count']


from django.contrib import admin
from .models import Category, Post, Add, Weather, SocialAccounts, FooterData


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['title', 'body']
    readonly_fields = ['views_count']
    prepopulated_fields = {'slug': ('title', )}
    exclude = ('search_vector', 'views_count', )


@admin.register(Add)
class AddAdmin(admin.ModelAdmin):
    list_display = ['image', 'url', 'is_active']
    readonly_fields = ['click_count']
    list_editable = ['is_active']


admin.site.register(Weather)
admin.site.register(SocialAccounts)
admin.site.register(FooterData)
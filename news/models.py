from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.created} || {self.title}"

    class Meta:
        ordering = ['-created']


class Add(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    url = models.URLField()
    click_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.url

    class Meta:
        ordering = ['is_active']




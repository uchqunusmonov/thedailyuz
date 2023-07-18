from aiogram import executor
from test import dp, post_news_to_channel
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def post_to_telegram(sender, instance, created, **kwargs):
    if created:
        photo = instance.image.path
        title = instance.title
        link = instance.get_absolute_url()
        executor.start(dp, post_news_to_channel(title, link, photo))
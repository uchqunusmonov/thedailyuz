import asyncio
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .api.v1.telegram_bot import post_news_to_channel


@receiver(post_save, sender=Post)
def post_to_telegram(sender, instance, created, **kwargs):
    if created:
        photo = instance.image.path
        title = instance.title
        link = instance.get_absolute_url()

        asyncio.run(post_news_to_channel(title, link, photo))
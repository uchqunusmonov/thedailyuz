import os
import asyncio
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Post
from .api.v1.telegram_bot import send_picture_and_link

def run_async_in_thread(func, *args, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = asyncio.ensure_future(func(*args, **kwargs))
    loop.run_until_complete(task)
    loop.close()


@receiver(post_save, sender=Post)
def post_to_telegram_channel(sender, instance, created, **kwargs):
    if created:
        channel_id = "@majburiy_fan_MATEMATIKA_rasmiy"

        picture_url = 'https://th.bing.com/th/id/R.6af6fd9c37f0de4abb34ea0fd20acce3?rik=55mqMmrTutVR0Q&pid=ImgRaw&r=0'

        link_url = f"{settings.INTERNAL_IPS[0]}{instance.get_absolute_url()}"

        link_text = instance.body[:50]
        
        run_async_in_thread(send_picture_and_link, channel_id, picture_url, link_text, link_url)

def post_to_telegram_async(*args, **kwargs):
    # This function will be used to call the asynchronous signal handling function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(post_to_telegram_channel(*args, **kwargs))
    loop.close()
import telegram
import os
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv
load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

bot = telegram.Bot(token=BOT_TOKEN)


async def post_news_to_channel(title, link, photo):
    message = f"{title}\n\n<a href='http://52.57.75.104{link}'>Batafsil o'qing</a>"
    await bot.send_photo(chat_id=CHANNEL_NAME, photo=photo, caption=message, parse_mode='html')

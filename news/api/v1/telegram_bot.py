import telegram
import os
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv
load_dotenv('.env')

BOT_TOKEN='1206930753:AAHngScrBXZOVExh4NDRnOO12_JA2T_P4_I'
CHANNEL_NAME='@majburiy_fan_MATEMATIKA_rasmiy'

bot = telegram.Bot(token=BOT_TOKEN)


async def post_news_to_channel(title, link, photo):
    message = f"{title}\n\n<a href='127.0.0.1:8000{link}'>Batafsil o'qing</a>"
    await bot.send_photo(chat_id=CHANNEL_NAME, photo=photo, caption=message, parse_mode='html')
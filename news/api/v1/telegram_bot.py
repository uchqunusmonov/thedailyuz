from aiogram import Bot, types
from django.conf import settings


async def send_picture_and_link(channel_id, picture_url, link_text, link_url):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    print("test")
    await bot.send_photo(channel_id, photo=picture_url, caption=link_text, parse_mode=types.ParseMode.HTML,
                         reply_markup=types.InlineKeyboardMarkup(
                             inline_keyboard=[[types.InlineKeyboardButton(text='Batafsil o\'qing', url=link_url)]]
                            )
                         ), print("test2")

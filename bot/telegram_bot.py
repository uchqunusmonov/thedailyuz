from aiogram import Bot, Dispatcher

BOT_TOKEN='1206930753:AAHngScrBXZOVExh4NDRnOO12_JA2T_P4_I'
CHANNEL_ID = "-1001344403669"
# CHANNEL_NAME='@majburiy_fan_MATEMATIKA_rasmiy'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def post_news_to_channel(title, link, photo):
    msg = f"{title}\n\n<a href='127.0.0.1:8000{link}'>Batafsil o'qing</a>" #mana yerga qara ahmoq, bu local host
    await bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=msg, parse_mode='html')
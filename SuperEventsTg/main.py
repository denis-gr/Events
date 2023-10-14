import os

import aiogram

import hanlders
from db import DB

TOKEN = os.environ.get("TG_TOKEN") or "6677981391:AAEkHT0-eaUSUkPyYav7S-Ahc44agm6Z3rQ"

async def start_bot():
    bot = aiogram.Bot(TOKEN)
    dp = aiogram.Dispatcher()
    dp.include_router(hanlders.dp)
    db = DB()
    await dp.start_polling(bot, db=db)


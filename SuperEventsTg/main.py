import os

import aiogram
from aiogram.fsm.storage.memory import MemoryStorage

import hanlders
from db import DB

TOKEN = os.environ.get("TG_TOKEN") or "6677981391:AAEkHT0-eaUSUkPyYav7S-Ahc44agm6Z3rQ"

async def start_bot():
    bot = aiogram.Bot(TOKEN)
    dp = aiogram.Dispatcher(storage=MemoryStorage())
    dp.include_router(hanlders.dp0)
    db = DB()
    await dp.start_polling(bot, db=db)


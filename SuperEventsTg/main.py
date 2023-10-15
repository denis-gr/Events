import os

import aiogram
from aiogram.fsm.storage.memory import MemoryStorage

import hanlders
from db import DB

TOKEN = os.environ.get("TG_TOKEN")

async def start_bot():
    bot = aiogram.Bot(TOKEN)
    dp = aiogram.Dispatcher(storage=MemoryStorage())
    dp.include_router(hanlders.dp0)
    db = DB()
    await dp.start_polling(bot, db=db)


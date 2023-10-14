import aiogram
import aiogram.types
import aiogram.filters

from db import DB
from texts import _

dp = aiogram.Router()

@dp.message(aiogram.filters.Command("start"))
async def cmd_start(mes: aiogram.types.Message, command: aiogram.filters.CommandObject):
    await mes.answer(_("start_mes"))


@dp.message(aiogram.filters.Command("get_public_events"))
async def cmd_get_public_events(mes: aiogram.types.Message, 
md: aiogram.filters.CommandObject, db: DB
):
    pass

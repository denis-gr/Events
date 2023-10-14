import aiogram
import aiogram.types

dp = aiogram.Router()

@dp.message()
async def echo(mes: aiogram.types.Message):
    await mes.answer(mes.text)


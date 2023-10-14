import aiogram
import aiogram.types
import aiogram.filters

from db import DB
from texts import _
from keyboards import get_choise_event_keyboard, ChoiseEventCallbackFactory, get_choise_event_hall_keyboard, ChoiseEventHallCallbackFactory, ChoiseHallPerfsCallbackFactory, get_choise_hall_perfs_keyboard

dp = aiogram.Router()

@dp.message(aiogram.filters.Command("start"))
async def cmd_start(mes: aiogram.types.Message, command: aiogram.filters.CommandObject):
    await mes.answer(_("start_mes"))


@dp.message(aiogram.filters.Command("get_public_events"))
async def cmd_get_public_events(mes: aiogram.types.Message, 
command: aiogram.filters.CommandObject, db: DB
):
    events = db.getAllEvents()
    if len(events): 
        events = events.iterrows()
        events = list(events)
        items = _("events_sep").join([_("events_item", event=v) for i, v in events])
        text = _("events", items=items)
        await mes.answer(text, reply_markup=get_choise_event_keyboard(events))
    else:
        await mes.answer(_("events_no"))


@dp.callback_query(ChoiseEventCallbackFactory.filter())
async def choise_event(callback: aiogram.types.CallbackQuery, 
db: DB, callback_data: ChoiseEventCallbackFactory):
    event = db.getEvent(callback_data.id)
    halls = db.getHallsFromEvent({ "path": [callback_data.path] })
    halls = halls.iterrows()
    halls = list(halls)
    await callback.message.edit_text(_("event", event=event), reply_markup=get_choise_event_hall_keyboard(halls))
    await callback.answer()


@dp.callback_query(ChoiseEventHallCallbackFactory.filter())
async def choise_event(callback: aiogram.types.CallbackQuery, 
db: DB, callback_data: ChoiseEventHallCallbackFactory):
    hall = db.getHall(callback_data.id)
    perfs = db.getPerformancesFromHall({ "path": [callback_data.path] })
    perfs = perfs.iterrows()
    perfs = list(perfs)
    await callback.message.edit_text(_("hall", hall=hall), reply_markup=get_choise_hall_perfs_keyboard(perfs))
    await callback.answer()


@dp.callback_query(ChoiseHallPerfsCallbackFactory.filter())
async def choise_event(callback: aiogram.types.CallbackQuery, 
db: DB, callback_data: ChoiseHallPerfsCallbackFactory):
    pref = db.getPerformances(callback_data.id)
    await callback.message.edit_text(_("pref", pref=pref), reply_markup=None) # TODO
    await callback.answer()  



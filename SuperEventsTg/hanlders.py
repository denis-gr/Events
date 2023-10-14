import random
import re

import aiogram
import aiogram.types
import aiogram.filters
from aiogram.fsm.context import FSMContext

from db import DB
from texts import _
from keyboards import get_choise_event_keyboard, ChoiseEventCallbackFactory, get_choise_event_hall_keyboard, ChoiseEventHallCallbackFactory, ChoiseHallPerfsCallbackFactory, get_choise_hall_perfs_keyboard, ChoiseEventGameCallbackFactory
from states import AnswerGamePointStatesGroup

dp0 = aiogram.Router()

@dp0.message(aiogram.filters.Command("start"))
async def cmd_start(mes: aiogram.types.Message,
command: aiogram.filters.CommandObject, db: DB, state: FSMContext,
):
    await state.clear()
    db.tryCreateTgUser(mes.from_user.id, mes.from_user.username)
    await mes.answer(_("start_mes"))
    typepage, id, extra = (command.args or "none-none").split("-")
    await {
        "event": choise_event_m,
        "hall": choise_hall_m,
        "performance": choise_pref_m,
        "game": choise_game_m,
        "none": lambda *args,  **kwargs: None
    }[typepage](mes, db=db, id=id)


dp = aiogram.Router()
dp.message.filter(not AnswerGamePointStatesGroup.answer)
dp2 = aiogram.Router()
dp2.message.filter(AnswerGamePointStatesGroup.answer)
dp0.include_router(dp)
dp0.include_router(dp2)


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
async def choise_event_cq(callback: aiogram.types.CallbackQuery, 
db: DB, callback_data: ChoiseEventCallbackFactory):
    event = db.getEvent(callback_data.id)
    halls = db.getHallsFromEvent({ "path": [callback_data.path] })
    halls = halls.iterrows()
    halls = list(halls)#TODO
    await callback.message.edit_text(_("event", event=event), reply_markup=get_choise_event_hall_keyboard(halls))
    await callback.answer()


async def choise_event_m(mes: aiogram.types.Message, 
db: DB, id: int):
    event = db.getEvent(id)
    halls = db.getHallsFromEvent(event)
    halls = halls.iterrows()
    halls = list(halls)
    games = db.getGamesFromEvent(event)
    games = games.iterrows()
    games = list(games)
    await mes.answer(_("event", event=event), reply_markup=get_choise_event_hall_keyboard(halls, games))


@dp.callback_query(ChoiseEventHallCallbackFactory.filter())
async def choise_hall_cq(callback: aiogram.types.CallbackQuery, 
db: DB, callback_data: ChoiseEventHallCallbackFactory):
    hall = db.getHall(callback_data.id)
    perfs = db.getPerformancesFromHall({ "path": [callback_data.path] })
    perfs = perfs.iterrows()
    perfs = list(perfs)
    await callback.message.edit_text(_("hall", hall=hall), reply_markup=get_choise_hall_perfs_keyboard(perfs))
    await callback.answer()


async def choise_hall_m(mes: aiogram.types.Message, 
db: DB, id: int):
    hall = db.getHall(id)
    perfs = db.getPerformancesFromHall(hall)
    perfs = perfs.iterrows()
    perfs = list(perfs)
    await mes.answer(_("hall", hall=hall), reply_markup=get_choise_hall_perfs_keyboard(perfs))


@dp.callback_query(ChoiseEventGameCallbackFactory.filter())
async def choise_game_cq(callback: aiogram.types.CallbackQuery, 
db: DB, callback_data: ChoiseEventGameCallbackFactory, state: FSMContext):
    game = db.getGame(callback_data.id)
    allgamepoints = list(db.getAllGamePoint(callback_data.id))
    curgamepoints = list(db.getGamePoint(callback.from_user.id, callback_data.id))
    allgp_l, curgp_l = len(allgamepoints), len(curgamepoints)
    not_av_ids = set([gp["point_hash"] for gp in curgamepoints])
    avaliable_gp = [gp for gp in allgamepoints if gp["id"] not in not_av_ids ]
    if avaliable_gp:
        gp = random.choices(avaliable_gp)
        if gp.get("Performance_or_hall"):
            r1 = db.getPerformances(gp["Performance_or_hall"])
            r2 = db.getHall(gp["Performance_or_hall"])
            r = r1.title[0] or r2.title[0] or None
            gp["Performance_or_hall"] = r
        await callback.message.edit_text(_("question", allgp_l=allgp_l, curgp_l=curgp_l, gp=gp), reply_markup=None) #Клава
        await callback.answer()
        if gp["answers"]: 
            await state.update_data(gp_id=gp["id"], game_id=callback_data.id)
            await state.set_state(AnswerGamePointStatesGroup.answer)
    else:
        await callback.message.edit_text(_("game_over"), reply_markup=None)
        await callback.answer()


async def choise_game_m(mes: aiogram.types.Message, 
db: DB, id: int, state: FSMContext):
    game = db.getGame(id)
    allgamepoints = list(db.getAllGamePoint(id))
    curgamepoints = list(db.getGamePoint(mes.from_user.id, mes.id))
    allgp_l, curgp_l = len(allgamepoints), len(curgamepoints)
    not_av_ids = set([gp["point_hash"] for gp in curgamepoints])
    avaliable_gp = [gp for gp in allgamepoints if gp["id"] not in not_av_ids ]
    if avaliable_gp:
        gp = random.choices(avaliable_gp)
        if gp.get("Performance_or_hall"):
            r1 = db.getPerformances(gp["Performance_or_hall"])
            r2 = db.getHall(gp["Performance_or_hall"])
            r = r1.title[0] or r2.title[0] or None
            gp["Performance_or_hall"] = r
        await mes.answer(_("question", allgp_l=allgp_l, curgp_l=curgp_l, gp=gp), reply_markup=None) #Клава
        if gp["answers"]: 
            await state.update_data(gp_id=gp["id"], game_id=id)
            await state.set_state(AnswerGamePointStatesGroup.answer)
    else:
        await mes.answer(_("game_over"), reply_markup=None)


@dp.callback_query(ChoiseHallPerfsCallbackFactory.filter())
async def choise_pref(callback: aiogram.types.CallbackQuery, 
db: DB, callback_data: ChoiseHallPerfsCallbackFactory):
    pref = db.getPerformances(callback_data.id)
    await callback.message.edit_text(_("pref", pref=pref), reply_markup=None) # TODO
    await callback.answer()  


async def choise_pref_m(mes: aiogram.types.Message, 
db: DB, id: int):
    pref = db.getPerformances(id)
    await mes.answer(_("pref", pref=pref), reply_markup=None) #TODO


@dp.message()
async def check_answer(mes: aiogram.types.Message, 
db: DB, state: FSMContext):
    data = await state.get_data()
    game = db.getGame(data.id)
    allgamepoints = list(db.getAllGamePoint(data.id))
    gp = [i for i in allgamepoints if i["id"] == date.gp_id][0]
    answer = re.sub(r"[^a-zA-Zа-яА-Я0-9]", "", mes.text.lower())
    for answerr in gp["answers"].split("\n"):
        answerr = re.sub(r"[^a-zA-Zа-яА-Я0-9]", "", answerr.lower())
        if answer == answerr:
            mes.answer(_("correct_answer"))
            db.markGP(mes.from_user.id, data.id, gp["id"])
            await state.clear()
            return choise_game_m(mes, db, data.id, state)
    else:
        mes.answer(_("incorrect_answer"))

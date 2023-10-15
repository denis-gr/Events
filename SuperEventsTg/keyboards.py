import aiogram.utils.keyboard
import aiogram.filters.callback_data

class ChoiseEventCallbackFactory(aiogram.filters.callback_data.CallbackData, prefix="ChoiseEvent"):
    id: str | int
    path: str | int


def get_choise_event_keyboard(events):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    for i, event in events:
        builder.button(text=event["title"],
            callback_data=ChoiseEventCallbackFactory(id=event["id"], path=event["path"]))
    builder.adjust(1)
    return builder.as_markup()


class ChoiseEventHallCallbackFactory(aiogram.filters.callback_data.CallbackData, prefix="ChoiseEventHall"):
    id: str | int
    path: str | int
    is_hall: bool


class ChoiseEventGameCallbackFactory(aiogram.filters.callback_data.CallbackData, prefix="ChoiseGameHall"):
    id: str | int
    path: str | int
    is_hall: bool


def get_choise_event_hall_keyboard(halls, games):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    for i, hall in halls:
        builder.button(text=hall["title"],
            callback_data=ChoiseEventHallCallbackFactory(id=hall["id"], path=hall["path"], is_hall=True))
    for i, hall in games:
        builder.button(text=hall["title"],
            callback_data=ChoiseEventGameCallbackFactory(id=hall["id"], path=hall["path"], is_hall=False))
    builder.adjust(1)
    return builder.as_markup()


class ChoiseHallPerfsCallbackFactory(aiogram.filters.callback_data.CallbackData, prefix="ChoiseHallPefrs"):
    id: str | int


def get_choise_hall_perfs_keyboard(halls):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    for i, pref in halls:
        builder.button(text=pref["title"],
            callback_data=ChoiseHallPerfsCallbackFactory(id=pref["id"]))
    builder.adjust(1)
    return builder.as_markup()

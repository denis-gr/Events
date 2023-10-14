messages = {
    "start_mes": "Привет! Я SuperEvents",
    "events": lambda items: f"""Текущие мероприятия:\n\n{items}""",
    "events_item": lambda event: f"{event.title}\n{event.description}",
    "events_sep": "\n",
    "events_no": "К сожалению открытых мероприятий пока нет",
    "event": lambda event: f"""{event.title[0]}\n{event.description[0]}""",
    "hall": lambda hall: f"""{hall.title[0]}\n{hall.description[0]}""",
    "pref": lambda pref: f"""{pref.title[0]}\n{pref.description[0]}""",
}


def _(key, **kwargs):
    message = messages.get(key)
    if not message:
        raise KeyError(f"'{key}' is not witten")
    elif isinstance(message, str):
        return message
    message = message(**kwargs)
    return message

__all__ = ["_"]



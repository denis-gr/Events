messages = {
    "start_mes": "Привет",
    "events": lambda items: f"""Текущие мероприятия:\n\n{items}""",
    "events_item": lambda event: f"{event.title}\n{event.description or ''}",
    "events_sep": "\n",
    "events_no": "К сожалению открытых мероприятий пока нет",
    "event": lambda event: f"""{event.title[0]}\n{event.description[0] or ''}""",
    "hall": lambda hall: f"""{hall.title[0]}\n{hall.description[0] or ''}""",
    "pref": lambda pref: f"""{pref.title[0]}\n{pref.description[0] or ''}""",
    "game_over": "Вы успешно прошли этот квест",
    "question": lambda allgp_l, curgp_l, gp: f"""Пройденно этапов: {curgp_l} / {allgp_l}
Текст этапа: {gp.get('text', 'Отсуствует')}
Место этапа: {gp.get('Performance_or_hall', 'Отсуствует')} #TODO
""",
    "correct_answer": "Правильно",
    "incorrect_answer": "Неправильно(\nПопробуйте ещё раз или перезапустите бота",
    "not_partisipatment": lambda title: f"Вы не были на {title}. Выполните /current_event, чтоб вернуться к мероприятию и выберете игру (при необходимости отсканируйте код мероприятия ещё раз)",
    "help_mes": "Используйте /get_public_events, что посметроть список открытых меропритий, /current_event, чтобы вернуться в мероприятию сканируйте QR коды, чтобы запиываться на закрытые меропрития и делать отметки об участии",
    "support_mes": "Пишите на wymefnxjqs@rambler.ru",
    "events_no_choise": "Вы ещё не выбрали мероприятия",
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



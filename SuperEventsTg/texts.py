messages = {
    "start_mes": "Привет! Я SuperEvents"
}


def _(key, **kwargs):
    message = messages.get(key)
    if not message:
        raise KeyError(f"'{key}' is not witten")
    elif isinstance(message, str):
        return message
    message = message(**kwargs)
    return messages

__all__ = ["_"]

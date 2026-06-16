from collections import defaultdict

from src.utils.ia.config import MAX_HISTORY


_memory = defaultdict(list)


def get_history(user_id: int):

    return _memory[user_id]


def add_message(
    user_id: int,

    role: str,

    content: str
):

    history = _memory[user_id]

    history.append({
        "role": role,

        "content": content
    })

    if len(history) > MAX_HISTORY:

        _memory[user_id] = history[-MAX_HISTORY:]


def clear_history(user_id: int):

    _memory[user_id] = []
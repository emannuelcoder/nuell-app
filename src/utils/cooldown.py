from datetime import datetime
from src.database.repositories.user_repository import get, setV

async def check(user_id: int):
    now = int(datetime.now().timestamp())

    cooldown = await get(user_id, "cooldown")

    if cooldown > now:
        return False, cooldown - now

    await setV(user_id, "cooldown", now + 5)

    return True, 0
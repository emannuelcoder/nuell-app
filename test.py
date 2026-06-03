import asyncio
from src.database.repositories.user_repository import get

async def test():
    cooldown = await get(
        949047304910942248,
        "daily_cd"
    )
    print(repr(cooldown))

asyncio.run(test())
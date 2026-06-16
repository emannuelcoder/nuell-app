from src.database.repositories.user_repository import get


async def get_ping(bot):

    return round(bot.latency * 1000)


async def get_commands_count(bot):

    return len(bot.tree.get_commands())


async def get_user_db(
    user_id: int,

    field: str
):

    return await get(user_id, field)


async def execute_tool(
    tool_name: str,

    *,

    bot=None,

    user=None,

    guild=None,

    channel=None
):

    try:

        match tool_name:

            case "ping":

                return {
                    "name": "ping",

                    "value": await get_ping(bot)
                }

            case "commands":

                return {
                    "name": "commands",

                    "value": await get_commands_count(bot)
                }

            case "balance":

                return {
                    "name": "balance",

                    "value": await get_user_db(
                        user.id,

                        "money"
                    )
                }

            case "premium":

                return {
                    "name": "premium",

                    "value": await get_user_db(
                        user.id,

                        "premium"
                    )
                }

            case "guild_name":

                return {
                    "name": "guild_name",

                    "value": guild.name
                }

            case "member_count":

                return {
                    "name": "member_count",

                    "value": guild.member_count
                }

            case _:

                return None

    except Exception:

        return None
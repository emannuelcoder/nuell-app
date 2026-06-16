import re

from src.utils.ia.config import (
    MODEL,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS
)

from src.utils.ia.prompts import SYSTEM_PROMPT

from src.utils.ia.memory import (
    get_history,
    add_message
)

from src.utils.ia.groq_client import client

from src.utils.ia.tools import execute_tool


TOOL_REGEX = r"<tool>(.*?)</tool>"


async def groq_service(
    *,
    bot,

    user_message: str,

    interaction=None,

    message=None
):

    if interaction:

        user = interaction.user

        guild = interaction.guild

        channel = interaction.channel

    else:

        user = message.author

        guild = message.guild

        channel = message.channel

    history = get_history(user.id)

    guild_name = guild.name if guild else "DM"

    guild_id = guild.id if guild else "N/A"

    guild_members = guild.member_count if guild else "N/A"

    channel_name = channel.name if guild else "DM"

    channel_id = channel.id

    context = f"""
Usuário:

Nome: {user.name}

Nome de exibição: {user.display_name}

Menção: {user.mention}

ID: {user.id}

Servidor:

Nome: {guild_name}

ID: {guild_id}

Membros: {guild_members}

Canal:

Nome: {channel_name}

ID: {channel_id}
"""

    messages = [
        {
            "role": "system",

            "content": SYSTEM_PROMPT
        },

        {
            "role": "system",

            "content": context
        },

        *history,

        {
            "role": "user",

            "content": user_message
        }
    ]

    response = await client.chat.completions.create(
        model=MODEL,

        messages=messages,

        temperature=TEMPERATURE,

        max_completion_tokens=MAX_OUTPUT_TOKENS
    )

    content = response.choices[0].message.content

    tool_match = re.search(
        TOOL_REGEX,

        content,

        re.IGNORECASE
    )

    if tool_match:

        tool_name = tool_match.group(1).strip()

        result = await execute_tool(
            tool_name,

            bot=bot,

            user=user,

            guild=guild,

            channel=channel
        )

        if result:

            messages.append({
                "role": "system",

                "content": f"""
Resultado:

{result["name"]}: {result["value"]}

Responda a pergunta original.

Não mencione ferramentas internas.
"""
            })

            response = await client.chat.completions.create(
                model=MODEL,

                messages=messages,

                temperature=TEMPERATURE,

                max_completion_tokens=MAX_OUTPUT_TOKENS
            )

            content = response.choices[0].message.content

    add_message(
        user.id,

        "user",

        user_message
    )

    add_message(
        user.id,

        "assistant",

        content
    )

    return content
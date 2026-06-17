import discord
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from src.utils.ia.service import groq_service
from src.utils.ia.config import MAX_INPUT_CHARS
from src.database.repositories.user_repository import get, setV

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="chat",
        description="Converse com a Nuell."
    )

    @app_commands.describe(
        mensagem="O que deseja perguntar ou falar."
    )

    async def chat(
        self,
        interaction: discord.Interaction,
        mensagem: str
    ):
        now = int(datetime.now().timestamp())

        cooldown = await get(
            interaction.user.id,
            "chat_cd"
        ) or 0

        if cooldown > now:
            return await interaction.response.send_message(
                (
                    f"## {emoji('gpt')} Inteligência Artificial\n"
                    f"> {emoji('pikachu_hello')} Olá, {interaction.user.mention}! Você já usou este comando recentemente.\n"
                    f"> {emoji('time')} Você poderá usar-lo novamente em **[ <t:{cooldown}:t> | <t:{cooldown}:R> ]**."
                ),
                ephemeral=True
            )

        await interaction.response.defer(
            thinking=True
        )

        try:
            if len(mensagem) > MAX_INPUT_CHARS:
                return await interaction.followup.send(
                    f"{emoji('error')} Sua mensagem é muito grande."
                )

            chat_cd = int(
                (
                    datetime.now()
                    + timedelta(seconds=30)
                ).timestamp()
            )

            await setV(
                interaction.user.id,
                "chat_cd",
                chat_cd
            )

            resposta = await groq_service(
                bot=self.bot,
                interaction=interaction,
                user_message=mensagem
            )

            if len(resposta) > 2000:
                resposta = resposta[:1997] + "..."

            await interaction.followup.send(
                resposta
            )

        except Exception as error:
            print(error)

            await interaction.followup.send(
                f"{emoji('ducos')} Ocorreu um erro ao conversar comigo."
            )

async def setup(bot):
    await bot.add_cog(
        Chat(bot)
    )
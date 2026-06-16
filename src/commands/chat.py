import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from src.utils.ia.service import groq_service
from src.utils.ia.config import MAX_INPUT_CHARS

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
        await interaction.response.defer(
            thinking=True
        )

        try:
            if len(mensagem) > MAX_INPUT_CHARS:
                return await interaction.followup.send(
                    f"{emoji('error')} Sua mensagem é muito grande."
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
import os
import json
import random
import discord
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji
from src.utils.random_message import random_message

class Message8Ball(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot, user: discord.Member, userMessage: str, botMessage: str):
        super().__init__()

        self.bot = bot
        self.user = user
        self.userMessage = userMessage
        self.botMessage = botMessage

        report = discord.ui.Button(
            label="Denunciar",
            custom_id="report",
            emoji=emoji('megafone'),
            style=discord.ButtonStyle.danger
        )

        self.add_item(
            discord.ui.TextDisplay(
                f"# {emoji('8ball')} Respostas aleatórias\n"
                f"> Mensagem do usuário: **{userMessage}**\n"
                f"> Minha resposta: **{botMessage}**\n"
                f"-# ⤷ {emoji('info')} Resposta requisitada por **{user.name}** usando o comando </8ball:1516566662432686202>.\n\n"
                f"-# {emoji('alfinete')} Caso o usuário enviou algo malicioso, não perca tempo, denuncie-o usando este botão!"
            )
        )

        self.add_item(discord.ui.ActionRow(report))

class Command8Ball(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="8ball",
        description="Receba uma resposta aleatória para sua mensagem"
    )

    @app_commands.describe(
        mensagem="Sua mensagem."
    )

    async def command8ball(self, interaction: discord.Interaction, mensagem: str):
        botMessage = random_message()

        await interaction.response.defer()
        await interaction.followup.send(
            view=Message8Ball(self.bot, interaction.user, mensagem, botMessage)
        )

async def setup(bot):
    await bot.add_cog(Command8Ball(bot))
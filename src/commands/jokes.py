import discord
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji
from src.utils.random_joke import random_joke

class jokeMessage(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot, user: discord.Member, joke: str, answer: str):
        super().__init__()

        self.bot = bot
        self.user = user
        self.joke = joke
        self.answer = answer

        self.add_item(
            discord.ui.TextDisplay(
                f"# {emoji('risada')} Piadas horríveis\n"
                f"> Piada: **{joke}**\n - Resposta: **{answer}**\n"
                f"-# ⤷ {emoji('info')} Piada requisitada por **{user.name}** usando o comando </piadas:1516572751224115292>.\n\n"
            )
        )

class jokeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="piadas",
        description="Receba uma piada aleatória"
    )

    async def jokecommand(self, interaction: discord.Interaction):
        piada, resposta = random_joke()

        await interaction.response.defer(thinking=True)
        await interaction.followup.send(
            view=jokeMessage(self.bot, interaction.user, piada, resposta)
        )

async def setup(bot):
    await bot.add_cog(jokeCommand(bot))
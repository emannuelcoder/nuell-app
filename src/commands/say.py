import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji

class SayMessage(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot, user: discord.User, message: str):
        super().__init__()
        
        self.bot = bot
        self.message = message
        self.user = user

        report = discord.ui.Button(
            label="Denunciar",
            custom_id="report",
            emoji=emoji('megafone'),
            style=discord.ButtonStyle.danger
        )

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('text')} Nova mensagem!\n"
                f"> Mensagem: **{message}**\n"
                f"-# ⤷ {emoji('info')} Mensagem enviada por **{user.name}** usando o comando </falar:1513696698277302333>.\n\n"
                f"-# {emoji('alfinete')} Caso este comando esteja sendo usado para algo malicioso, benefício próprio, divulgação, flood/spam ou a infração de regras deste servidor, não perca tempo, denuncie-o usando este botão!"
            )
        )

        self.add_item(discord.ui.ActionRow(report))

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="falar",
        description="Envie uma mensagem pelo bot"
    )

    @app_commands.describe(
        texto="Texto a ser reenviado."
    )

    async def say(self, interaction: discord.Interaction, texto: str):
        await interaction.response.defer()
        await interaction.followup.send(
            view=SayMessage(self.bot, interaction.user, texto)
        )

async def setup(bot):
    await bot.add_cog(Say(bot))
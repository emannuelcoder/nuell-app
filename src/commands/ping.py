import discord
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Veja a latência do bot."
    )

    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"## {emoji('pong')} Pong!\n> Olá, {interaction.user.mention}! Minha latência atual é de **[ `{latency}ms` ].**")

async def setup(bot):
    await bot.add_cog(Ping(bot))
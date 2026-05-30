import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        bot_mention = self.bot.user.mention
        bot_name = self.bot.user.name.lower()

        if not message.author.bot:
            if message.content == bot_mention or message.content.lower() == bot_name:
                await message.reply(f"## 👋 Olá, {message.author.mention}!\n> Eu sou o **{self.bot.user.name}**, uma aplicação feita para divertir e gerenciar seu servidor! Para mais informações acesse meu **[WebSite](<https://nuell.netlify.app/>)** ou use o comando **[ `/ajuda` ]**\n-# 📌 Use os botões abaixo para entrar em **site** ou **comunidade**!")

async def setup(bot):
    await bot.add_cog(OnMessage(bot))

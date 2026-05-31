import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MentionMessage(discord.ui.LayoutView):
        def __init__(self, message: discord.Message, bot):
            super().__init__()

            self.add_item(
                discord.ui.TextDisplay(
                    f"## 👋 Olá, {message.author.mention}!\n"
                    f"> Eu sou o **{bot.user.name}**, uma aplicação feita para divertir e gerenciar seu servidor!"
                    f"Para mais informações acesse meu Website ou use o comando **`/ajuda`**.\n"
                    f"-# 📌 Use os botões abaixo para entrar em **site**, **comunidade** ou me **adicionar**!"
                )
            )

            row = discord.ui.ActionRow(
                discord.ui.Button(
                    label="Site",
                    url="https://nuell.netlify.app/"
                ),
                discord.ui.Button(
                    label="Comunidade",
                    url="https://discord.gg/nuell"
                )
            )

            self.add_item(row)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.strip().lower() == self.bot.user.mention.lower():
            await message.reply(
                view=self.MentionMessage(message, self.bot)
            )

async def setup(bot):
    await bot.add_cog(OnMessage(bot))
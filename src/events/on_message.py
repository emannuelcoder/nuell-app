import discord
from discord.ext import commands
from src.utils.emojis import emoji

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MentionMessage(discord.ui.LayoutView):
        def __init__(self, message: discord.Message, bot, help_id: int):
            super().__init__()

            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('pikachu_hello')} Olá, {message.author.mention}!\n"
                    f"> Eu sou o **{bot.user.name}**, uma aplicação feita para divertir e gerenciar seu servidor!\n"
                    f"> Para mais informações acesse meu Website ou use o comando **</ajuda:{help_id}>**.\n"
                    f"-# {emoji('alfinete')} Use os botões abaixo para entrar em **site**, **comunidade** ou me **adicionar**!"
                )
            )

            row = discord.ui.ActionRow(
                discord.ui.Button(
                    label="Site",
                    url="https://nuell-app.netlify.app/",
                    emoji=emoji("website")
                ),
                discord.ui.Button(
                    label="Comunidade",
                    url="https://discord.gg/CUv9QAxJPa",
                    emoji=emoji("discord")
                ),
                discord.ui.Button(
                    label="Adicionar",
                    url="https://discord.com/oauth2/authorize?client_id=1510408439694889140&permissions=8&integration_type=0&scope=bot",
                    emoji=emoji("add")
                )
            )

            self.add_item(row)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.content.strip() == self.bot.user.mention:
            commands_list = await self.bot.tree.fetch_commands()

            help_command = discord.utils.get(
                commands_list,
                name="ajuda"
            )

            help_id = help_command.id if help_command else 0

            await message.reply(
                view=self.MentionMessage(message, self.bot, help_id)
            )

async def setup(bot):
    await bot.add_cog(OnMessage(bot))
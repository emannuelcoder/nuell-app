import discord
from discord.ext import commands
from src.utils.ia.service import groq_service
from src.utils.ia.config import MAX_INPUT_CHARS
from src.utils.emojis import emoji

class ChatReply(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot

        if not hasattr(
            bot,
            "active_chats"
        ):
            bot.active_chats = set()


    @commands.Cog.listener()

    async def on_message(
        self,
        message: discord.Message
    ):

        if message.author.bot:
            return

        if not message.reference:
            return

        if message.author.id not in self.bot.active_chats:
            return

        try:
            replied = await message.channel.fetch_message(
                message.reference.message_id
            )

        except:
            return

        if replied.author.id != self.bot.user.id:
            return

        if len(message.content) > MAX_INPUT_CHARS:
            return await message.reply(
                f"{emoji('error')} Sua mensagem é muito grande."
            )

        async with message.channel.typing():
            try:
                resposta = await groq_service(
                    bot=self.bot,
                    message=message,
                    user_message=message.content
                )

                if len(resposta) > 2000:
                    resposta = resposta[:1997] + "..."

                await message.reply(
                    resposta
                )

            except Exception as error:
                print(error)
                await message.reply(
                    f"{emoji('error')} Ocorreu um erro."
                )

async def setup(bot):
    await bot.add_cog(
        ChatReply(bot)
    )
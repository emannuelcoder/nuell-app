import random
import io
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji

class Message(discord.ui.LayoutView):
    def __init__(
        self,
        bot: commands.Bot,
        target1: discord.Member,
        target2: discord.Member,
        percent: int,
        text: str
    ):
        super().__init__()

        self.bot = bot

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('heart')} Vai dar namoro\n"
                f"> A compatibilidade de {target1.mention} e {target2.mention} é de **{percent}%**\n"
                f"-# {text}"
            )
        )

class Ship(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="combinar",
        description="Combine e veja a compatibilidade de 2 pessoas"
    )
    @app_commands.describe(
        usuário1="Primeiro usuário a ser combinado",
        usuário2="Segundo usuário a ser combinado"
    )
    async def ship(
        self,
        interaction: discord.Interaction,
        usuário1: discord.Member,
        usuário2: discord.Member | None = None
    ):
        user1 = usuário1
        user2 = usuário2 or interaction.user

        if user1.id == 1510408439694889140 or user2.id == 1510408439694889140:
            await interaction.response.send_message(
                f"{emoji('error')} Vou mandar a real para ti, nossa compatibilidade é de **0%**. Nunca irei namorar alguém como você, sinto muito."
            )
            return

        await interaction.response.defer(thinking=True)

        percent = random.randint(0, 100)

        if percent == 0:
            text = "Deus me livre, junto esses não fica não!"
        elif percent < 15:
            text = "Acho melhor serem apenas amigos."
        elif percent < 40:
            text = "Se organizar direitinho pode dar certo!"
        elif percent < 60:
            text = "Tem uma boa chance de se tornarem namorados!"
        elif percent < 80:
            text = "Já é quase confirmado né."
        elif percent < 100:
            text = "Esses vão ser o casal com mais compatibilidade."
        else:
            text = "Nem eu e meu criador somos assim... Quando acontece o casamento?"

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.popcat.xyz/v2/ship?user1={user1.display_avatar.url}&user2={user2.display_avatar.url}"
            ) as response:

                if response.status != 200:
                    await interaction.followup.send(
                        f"{emoji('error')} Erro ao gerar imagem de ship."
                    )
                    return

                image_bytes = await response.read()

        file = discord.File(
            fp=io.BytesIO(image_bytes),
            filename="ship.png"
        )

        await interaction.followup.send(
            file=file,
            view=Message(
                self.bot,
                user1,
                user2,
                percent,
                text
            )
        )

async def setup(bot):
    await bot.add_cog(Ship(bot))
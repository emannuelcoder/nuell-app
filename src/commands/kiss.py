import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji

class KissMessage(discord.ui.LayoutView):

    def __init__(
        self,
        bot: commands.Bot,
        author: discord.User,
        target: discord.Member,
        image_url: str
    ):
        super().__init__()

        self.bot = bot
        self.author = author
        self.target = target

        message = f"**{author.mention}** beijou **{target.mention}**." if target.id != author.id else f"**{author.mention} se beijou! Acho que foi pelo espelho {emoji('risada')}**"

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('heart')} Beijo\n"
                f"> {message}\n"
            )
        )

        self.add_item(
            discord.ui.MediaGallery(
                discord.MediaGalleryItem(
                    media=image_url
                )
            )
        )

class Kiss(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="beijar",
        description="Beije um usuário."
    )

    @app_commands.describe(
        usuario="Usuário que receberá o beijo."
    )

    async def kiss(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member
    ):
        if usuario.id == 1510408439694889140:
            await interaction.response.send_message(f"{emoji('error')} Cara aceita, ninguém te quer, um deles sou eu, não vou te beijar.")
            return
        
        await interaction.response.defer(thinking=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://nekos.best/api/v2/kiss"
            ) as response:

                data = await response.json()

        image_url = data["results"][0]["url"]

        await interaction.followup.send(
            view=KissMessage(
                self.bot,
                interaction.user,
                usuario,
                image_url
            )
        )

async def setup(bot):
    await bot.add_cog(Kiss(bot))
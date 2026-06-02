import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji

class DailyMessage(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('gift')} Recompensa Diária\n"
                f"> {emoji('pikachu_hello')} Olá, {interaction.user.mention}! Aqui você pode resgatar sua recompensa diária, apenas clicando no botão **[ `\"Resgatar\"` ]**.\n"
                f"Resgatando sua recompensa, você pode ganhar entre **[ `2000` ]** e **[ `8000` ] {emoji('ducos')} Ducos**.\n"
                f"> {emoji('premium')} Sabia que usuários **premiums** tem mais vantagens? Premium passar a receber um bônus de **[ `5000` ] {emoji('ducos')} Ducos**.\n"
                f"-# {emoji('time')} Lembre-se: você poderá resgatar sua recompensa novamente às **[ `00:01` ]**."
            )
        )

        row = discord.ui.ActionRow(
            discord.ui.Button(
                label="Resgatar",
                style=discord.ButtonStyle.success,
                custom_id=f"daily_{interaction.user.id}",
                emoji=emoji('gift')
            )
        )
        self.add_item(row)

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="daily",
        description="Resgate sua recompensa diária"
    )

    async def daily(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            view=DailyMessage(interaction)
        )

async def setup(bot):
    await bot.add_cog(Daily(bot))
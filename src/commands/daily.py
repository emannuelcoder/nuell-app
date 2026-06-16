import discord
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from src.database.repositories.user_repository import get

class DailyMessage(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction, cooldown: int):
        super().__init__()

        now_dt = datetime.now()
        now = int(now_dt.timestamp())

        midNight = now_dt.replace(
            hour=0,
            minute=1,
            second=0,
            microsecond=0
        )

        if now_dt >= midNight:
            midNight += timedelta(days=1)

        midNight = int(midNight.timestamp())

        if cooldown > now:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('gift')} Recompensa Diária\n"
                    f"> {emoji('pikachu_hello')} Olá, {interaction.user.mention}! Você já resgatou sua recompensa diária hoje.\n"
                    f"> {emoji('time')} Você poderá resgatar sua recompensa novamente em **[ <t:{cooldown}:t> | <t:{cooldown}:R> ]**."
                )
            )
            row = discord.ui.ActionRow(
                discord.ui.Button(
                    label="Já resgatado!",
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"daily_{interaction.user.id}",
                    emoji=emoji('check'),
                    disabled=True
                )
            )
            self.add_item(row)

        else:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('gift')} Recompensa Diária\n"
                    f"> {emoji('pikachu_hello')} Olá, {interaction.user.mention}! Aqui você pode resgatar sua recompensa diária, apenas clicando no botão **[ `\"Resgatar\"` ]**.\n"
                    f"Resgatando sua recompensa, você pode ganhar entre **[ `2000` ]** e **[ `8000` ] {emoji('ducos')} Ducos**.\n"
                    f"-# ⤷ {emoji('time')} Lembre-se: você poderá resgatar sua recompensa novamente às **[ <t:{midNight}:t> | <t:{midNight}:R> ]**."
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
        name="diário",
        description="Resgate sua recompensa diária"
    )

    async def daily(self, interaction: discord.Interaction):
        cooldown = await get(interaction.user.id, "daily_cd") or 0

        await interaction.response.send_message(
            view=DailyMessage(interaction, cooldown)
        )

async def setup(bot):
    await bot.add_cog(Daily(bot))
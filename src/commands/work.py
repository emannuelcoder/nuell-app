import discord
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from src.utils.cooldown import check
from src.database.repositories.user_repository import get

class WorkMessage(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction, cooldown: int):
        super().__init__()

        now_dt = datetime.now()
        now = int(now_dt.timestamp())

        min30 = now_dt + timedelta(minutes=30)
        min30 = int(min30.timestamp())

        if cooldown > now:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('work')} Trabalho\n"
                    f"> {emoji('pikachu_hello')} Olá, {interaction.user.mention}! Você trabalhou recentemente.\n"
                    f"> {emoji('time')} Você poderá trabalhar novamente em **[ <t:{cooldown}:t> | <t:{cooldown}:R> ]**."
                )
            )
            row = discord.ui.ActionRow(
                discord.ui.Button(
                    label="Você já trabalhou!",
                    style=discord.ButtonStyle.secondary,
                    custom_id=f"work_{interaction.user.id}",
                    emoji=emoji('check'),
                    disabled=True
                )
            )
            self.add_item(row)

        else:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('work')} Trabalho\n"
                    f"> {emoji('pikachu_hello')} Olá, {interaction.user.mention}! Aqui você pode trabalhar, apenas clicando no botão **[ `\"Trabalhar\"` ]**.\n"
                    f"Trabalhando, você pode ganhar entre **[ `800` ]** e **[ `2500` ] {emoji('ducos')} Ducos**.\n"
                    f"-# ⤷ {emoji('time')} Lembre-se: você poderá trabalhar novamente às **[ <t:{min30}:t> | <t:{min30}:R> ]**."
                )
            )
            row = discord.ui.ActionRow(
                discord.ui.Button(
                    label="Trabalhar",
                    style=discord.ButtonStyle.success,
                    custom_id=f"work_{interaction.user.id}",
                    emoji=emoji('work')
                )
            )
            self.add_item(row)

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="trabalhar",
        description="Trabalhe e ganhe ducos"
    )

    async def work(self, interaction: discord.Interaction):
        can_use, remaining = await check(interaction.user.id)

        if not can_use:
            await interaction.response.send_message(
                f"{emoji('time')} Aguarde **{remaining}s** antes de usar outro comando.",
                ephemeral=True
            )
            return
        
        cooldown = await get(interaction.user.id, "work_cd") or 0

        await interaction.response.send_message(
            view=WorkMessage(interaction, cooldown)
        )

async def setup(bot):
    await bot.add_cog(Work(bot))
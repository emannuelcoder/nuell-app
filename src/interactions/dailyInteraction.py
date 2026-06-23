import discord
import random
from datetime import datetime, timedelta
from discord.ext import commands
from src.utils.emojis import emoji
from src.database.repositories.user_repository import setV, get, add
from src.utils.abbreviate import abv

class InteractionMessage(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction, amount: int, total: int):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('gift')} Recompensa Diária\n"
                f"> {emoji('check')} {interaction.user.mention}, você resgatou sua **recompensa diária** com sucesso e ganhou **[ `{amount}` | `{abv(amount)}` ] {emoji('ducos')} Ducos**.\n"
                f"-# ⤷ Você pode usar </saldo:1513679777410846854> para consultar seu novo saldo de ducos."
            )
        )

        row = discord.ui.ActionRow(
            discord.ui.Button(
                label="Resgatado!",
                style=discord.ButtonStyle.secondary,
                disabled=True,
                emoji=emoji('check')
            )
        )
        self.add_item(row)

class DailyInteraction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return
        
        if not interaction.data:
            return
        
        custom_id = interaction.data.get("custom_id")
        if not custom_id:
            return

        data = custom_id.split("_")
        if data[0] != "daily":
            return
        
        if interaction.user.id != int(data[1]):
            return await interaction.response.send_message(
                f"{emoji('error')} Erro, {interaction.user.mention}. Você não pode apertar este botão, afinal, ele não é seu. Cai fora!",
                ephemeral=True
            )

        amount = random.randint(2000, 8000)
        await add(interaction.user.id, 'money', amount)
        total = await get(interaction.user.id, 'money')

        cooldown = await get(interaction.user.id, "daily_cd")
        now_dt = datetime.now()
        now = int(now_dt.timestamp())

        if cooldown > now:
            await interaction.response.send_message(f"{emoji('error')} Tá tentando burlar meu sistema? Tem que esperar direitinho viu.")

        midNight = now_dt.replace(
            hour=0,
            minute=1,
            second=0,
            microsecond=0
        )

        if now_dt >= midNight:
            midNight += timedelta(days=1)

        midNight = int(midNight.timestamp())

        await setV(interaction.user.id, 'daily_cd', midNight)

        await interaction.response.edit_message(
            view=InteractionMessage(interaction, amount, total)
        )

async def setup(bot):
    await bot.add_cog(DailyInteraction(bot))
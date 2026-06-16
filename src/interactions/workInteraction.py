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
                f"## {emoji('work')} Trabalho\n"
                f"> {emoji('check')} {interaction.user.mention}, você trabalhou com sucesso e ganhou **[ `{amount}` | `{abv(amount)}` ] {emoji('ducos')} Ducos**.\n"
                f"-# ⤷ Você pode usar </saldo:1513679777410846854> para consultar seu novo saldo de ducos."
            )
        )

        row = discord.ui.ActionRow(
            discord.ui.Button(
                label="Você trabalhou!",
                style=discord.ButtonStyle.secondary,
                disabled=True,
                emoji=emoji('check')
            )
        )
        self.add_item(row)

class WorkInteraction(commands.Cog):
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
        if data[0] != "work":
            return
        
        if interaction.user.id != int(data[1]):
            return await interaction.response.send_message(
                f"{emoji('error')} Erro, {interaction.user.mention}. Você não pode apertar este botão, afinal, ele não é seu. Cai fora!",
                ephemeral=True
            )

        amount = random.randint(800, 2500)
        await add(interaction.user.id, 'money', amount)
        total = await get(interaction.user.id, 'money')

        now_dt = datetime.now()
        now = int(now_dt.timestamp())

        min30 = now_dt + timedelta(minutes=30)
        min30 = int(min30.timestamp())

        await setV(interaction.user.id, 'work_cd', min30)

        await interaction.response.edit_message(
            view=InteractionMessage(interaction, amount, total)
        )

async def setup(bot):
    await bot.add_cog(WorkInteraction(bot))
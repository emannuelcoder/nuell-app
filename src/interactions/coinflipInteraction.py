import random
import discord
from discord.ext import commands
from src.utils.emojis import emoji
from src.utils.parse import parse
from src.utils.abbreviate import abv
from src.database.repositories.user_repository import get, setV, add, sub
from src.utils.cooldown import check

class CoinflipInteraction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        if interaction.type != discord.InteractionType.component:
            return

        custom_id = interaction.data.get("custom_id")
        if not custom_id:
            return

        data = custom_id.split("_")

        if data[0] != "coinflip":
            return

        action = data[1]

        if action == "cancel":
            user_id = int(data[2])

            if interaction.user.id != user_id:
                return await interaction.response.send_message(
                    f"{emoji('error')} Ei, {interaction.user.mention}. Este botão não é para você.",
                    ephemeral=True
                )

            await setV(user_id, "in_bet", False)

            view = discord.ui.LayoutView()
            view.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('check')} Aposta cancelada\n"
                    f"> {interaction.user.mention}, sua aposta foi cancelada com sucesso.\n"
                    f"{emoji('info')} Você já pode apostar novamente."
                )
            )

            return await interaction.response.edit_message(view=view)

        if action == "play":
            if len(data) != 5:
                return

            user_id = int(data[2])
            amount = parse(data[3])
            choice = data[4].lower()

            if interaction.user.id != user_id:
                return await interaction.response.send_message(
                    f"{emoji('error')} Ei, {interaction.user.mention}. Este botão não é para você.",
                    ephemeral=True
                )
            
            can_use, remaining = await check(interaction.user.id)

            if not can_use:
                await interaction.response.send_message(
                    f"{emoji('time')} Aguarde **{remaining}s** antes de usar outro comando.",
                    ephemeral=True
                )
                return

            user_money = await get(user_id, "money")

            if user_money < amount:
                await setV(user_id, "in_bet", False)

                return await interaction.response.send_message(
                    f"{emoji('error')} Você não possui saldo suficiente para realizar esta aposta.",
                    ephemeral=True
                )

            result = random.choice(["cara", "coroa"])

            win = result == choice

            if win:
                reward = amount * 2
                await add(user_id, "money", reward)
            else:
                reward = 0
                await sub(user_id, "money", amount)

            await setV(user_id, "in_bet", False)

            if win:
                msg = (
                    f"## {emoji('moeda')} Coinflip\n"
                    f"> {interaction.user.mention}, você apostou **{amount} {emoji('ducos')} Ducos** e "
                    f"**ganhou [ `{reward}` | `{abv(reward)}` ] Ducos**.\n\n"
                    f"{emoji('confetes')} Você acertou o lado da moeda e dobrou sua aposta!\n"
                    f"-# ⤷ Use </saldo:1513679777410846854> para ver seu novo saldo."
                )
            else:
                msg = (
                    f"## {emoji('moeda')} Coinflip\n"
                    f"> {interaction.user.mention}, você apostou **[ `{amount}`| `{abv(amount)}` ] {emoji('ducos')} Ducos** e "
                    f"**perdeu {amount} Ducos**.\n\n"
                    f"{emoji('choro')} Você errou o lado da moeda e perdeu sua aposta.\n"
                    f"-# ⤷ Use </saldo:1513679777410846854> para ver seu saldo."
                )

            view = discord.ui.LayoutView()
            view.add_item(discord.ui.TextDisplay(msg))

            return await interaction.response.edit_message(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(CoinflipInteraction(bot))
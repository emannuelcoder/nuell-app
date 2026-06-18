import random
import discord
from discord.ext import commands
from src.utils.emojis import emoji
from src.utils.parse import parse
from src.database.repositories.user_repository import get, setV, add, sub
from src.utils.abbreviate import abv

class InteractionMessage(discord.ui.LayoutView):
    def __init__(
        self,
        user: discord.User,
        amount: int,
        reward: int,
        win: bool
    ):
        super().__init__(timeout=None)

        if win:
            message = (
                f"## {emoji('slots')} Máquina caça-níqueis\n"
                f"> {user.mention}, você apostou **{amount} {emoji('ducos')} Ducos** e **ganhou [ {reward} | {abv(reward)} ] Ducos**.\n\n"
                f"{emoji('confetes')} Parabéns! Você conseguiu vencer na máquina caça-níqueis e ganhou **{reward} Ducos**.\n"
                f"-# ⤷ Você pode usar </saldo:1513679777410846854> para consultar seu novo saldo."
            )
        else:
            message = (
                f"## {emoji('slots')} Máquina caça-níqueis\n"
                f"> {user.mention}, você apostou **{amount} {emoji('ducos')} Ducos** e **perdeu {amount} Ducos**.\n\n"
                f"{emoji('choro')} A vida é assim, feita de escolhas. E você fez a escolha errada... Bobão, perdeu **{amount} Ducos**.\n"
                f"-# ⤷ Você pode usar </saldo:1513679777410846854> para consultar seu novo saldo."
            )

        self.add_item(
            discord.ui.TextDisplay(message)
        )

class CancelMessage(discord.ui.LayoutView):
    def __init__(
        self,
        user: discord.User
    ):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('check')} Aposta cancelada\n"
                f"> {user.mention}, sua aposta foi cancelada.\n"
                f"{emoji('info')} A aposta foi cancelada com sucesso!.\n\n"
                f"> Se acreditar que houve algum erro, entre em contato com nossa equipe através do suporte."
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Suporte",
                    style=discord.ButtonStyle.link,
                    url="https://discord.gg/CUv9QAxJPa"
                )
            )
        )

class SlotsInteraction(commands.Cog):
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

        if len(data) < 3:
            return

        if data[0] != "slots":
            return

        action = data[1]

        if action == "cancel":
            user_id = int(data[2])

            if interaction.user.id != user_id:
                return await interaction.response.send_message(
                    f"{emoji('error')} Ei, {interaction.user.mention}. Este botão não é para você. Cai fora!",
                    ephemeral=True
                )

            await setV(user_id, "in_bet", False)

            view = CancelMessage(
                interaction.user
            )

            return await interaction.response.edit_message(
                view=view
            )

        if action == "play":
            if len(data) != 4:
                return

            user_id = int(data[2])

            if interaction.user.id != user_id:
                return await interaction.response.send_message(
                    f"{emoji('error')} Ei, {interaction.user.mention}. Este botão não é para você. Cai fora!",
                    ephemeral=True
                )

            win = random.randint(1, 100) <= 45

            amount = 0
            reward = 0
            if win:
                try:
                    amount = parse(data[3])
                    reward = amount * 3
                except ValueError:
                    await setV(user_id, "in_bet", False)
                    return

            else:
                try:
                    amount = parse(data[3])
                except ValueError:
                    await setV(user_id, "in_bet", False)
                    return
                
            user_money = await get(user_id, "money")

            if user_money < amount:
                await setV(user_id, "in_bet", False)

                return await interaction.response.send_message(
                    f"{emoji('error')} Você não possui saldo suficiente para realizar esta aposta.",
                    ephemeral=True
                )
            
            if win:
                await add(user_id, "money", reward)
            else:
                await sub(user_id, "money", amount)

            await setV(user_id, "in_bet", False)

            view = InteractionMessage(
                interaction.user,
                amount,
                reward,
                win
            )

            await interaction.response.edit_message(
                view=view
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(SlotsInteraction(bot))
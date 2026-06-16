import discord
from discord.ext import commands

from src.utils.emojis import emoji
from src.utils.abbreviate import abv
from src.database.repositories.user_repository import setV


class InteractionMessage(discord.ui.LayoutView):
    def __init__(
        self,
        amount: int,
        sender: discord.User,
        target: discord.User,
        user: discord.User
    ):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('check')} Pagamento cancelado\n"
                f"> {sender.mention}, sua transferência de **[ `{amount}` | `{abv(amount)}` ] {emoji('ducos')} Ducos** para {target.mention} foi cancelada.\n"
                f"{emoji('info')} O pagamento foi cancelado por {user.mention}.\n\n"
                f"> Se acreditar que houve algum erro, entre em contato com nossa equipe através do suporte."
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Suporte",
                    style=discord.ButtonStyle.link,
                    url="https://discord.gg/support"
                )
            )
        )


class PayCancelInteraction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(
        self,
        interaction: discord.Interaction
    ):
        if interaction.type != discord.InteractionType.component:
            return

        if not interaction.data:
            return

        custom_id = interaction.data.get("custom_id")

        if not custom_id:
            return

        data = custom_id.split("_")

        if len(data) != 5:
            return

        if data[0] != "pay" or data[1] != "cancel":
            return

        sender_id = int(data[2])
        target_id = int(data[3])
        amount = int(data[4])

        if interaction.user.id not in (sender_id, target_id):
            return await interaction.response.send_message(
                f"{emoji('error')} Ei, {interaction.user.mention}. Esse pagamento não pertence a você. Cai fora!",
                ephemeral=True
            )

        sender = self.bot.get_user(sender_id)

        if sender is None:
            sender = await self.bot.fetch_user(sender_id)

        target = self.bot.get_user(target_id)

        if target is None:
            target = await self.bot.fetch_user(target_id)

        await setV(sender_id, "in_pay", False)

        await interaction.response.edit_message(
            view=InteractionMessage(
                amount,
                sender,
                target,
                interaction.user
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(
        PayCancelInteraction(bot)
    )
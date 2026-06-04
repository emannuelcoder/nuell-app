import discord
from discord.ext import commands
from src.utils.emojis import emoji
from src.utils.abbreviate import abv
from src.database.repositories.user_repository import add, sub, setV

class InteractionMessage(discord.ui.LayoutView):
    def __init__(
        self,
        interaction: discord.Interaction,
        amount: int,
        sender: discord.User,
        target: discord.User
    ):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('check')} Pagamento realizado\n"
                f"> {sender.mention}, sua transferência de **{abv(amount)} {emoji('ducos')} Ducos** para {target.mention} foi concluída com sucesso.\n"
                f"{emoji('info')} O valor já foi processado e enviado para o destinatário.\n\n"
                f"-# ⤷ Você pode verificar seu novo saldo usando o commando `/ducos atm`.\n"
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Transferência concluída",
                    style=discord.ButtonStyle.secondary,
                    disabled=True,
                    emoji=emoji("check")
                )
            )
        )

class PayInteraction(commands.Cog):
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

        if data[0] != "pay" or data[1] != "accept":
            return

        sender_id = int(data[2])
        target_id = int(data[3])
        amount = int(data[4])

        sender = self.bot.get_user(sender_id)
        target = self.bot.get_user(target_id)

        if sender is None:
            sender = await self.bot.fetch_user(sender_id)

        if target is None:
            target = await self.bot.fetch_user(target_id)

        if interaction.user.id not in (sender_id, target_id):
            return await interaction.response.send_message(
                f"{emoji('error')} Ei, {interaction.user.mention}. Esse pagamento não pertence a você.",
                ephemeral=True
            )
        
        payed = "/"
        parts = payed.split("/")
        if interaction.user.id == sender_id:
            if parts[0] == "sender":
                return await interaction.response.send_message(
                    f"{emoji('error')} {interaction.user.mention}, você já aceitou esse pagamento, {target.mention} aceitar.",
                    ephemeral=True
                )
            elif not parts[0]:
                parts[0] = "sender"
            elif parts[0] == "target":
                parts[1] = "sender"
        
        if interaction.user.id == target_id:
            if parts[0] == "target":
                return await interaction.response.send_message(
                    f"{emoji('error')} {interaction.user.mention}, você já aceitou esse pagamento, {sender.mention} aceitar.",
                    ephemeral=True
                )
            elif not parts[0]:
                parts[0] = "target"
            elif parts[0] == "sender":
                parts[1] = "target"

        payed = "/".join(parts)
        
        await add(target_id, "money", amount)
        await sub(sender_id, "money", amount)
        await setV(sender_id, "in_pay", False)

        await interaction.response.edit_message(
            view=InteractionMessage(
                interaction,
                amount,
                sender,
                target
            )
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(
        PayInteraction(bot)
    )
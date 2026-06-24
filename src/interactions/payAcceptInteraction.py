import discord
from discord.ext import commands
from src.utils.emojis import emoji
from src.utils.abbreviate import abv
from src.database.repositories.user_repository import add, sub, setV
from src.utils.cooldown import check

class InteractionMessage(discord.ui.LayoutView):
    def __init__(
        self,
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
                f"-# ⤷ Você pode usar </saldo:1513679777410846854> para consultar seu novo saldo de ducos.\n"
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

class PayAcceptInteraction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.accepted = {}

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

        key = f"{sender_id}_{target_id}_{amount}"

        sender = self.bot.get_user(sender_id)
        target = self.bot.get_user(target_id)

        if sender is None:
            sender = await self.bot.fetch_user(sender_id)

        if target is None:
            target = await self.bot.fetch_user(target_id)

        can_use, remaining = await check(interaction.user.id)

        if not can_use:
            await interaction.response.send_message(
                f"{emoji('time')} Aguarde **{remaining}s** antes de usar outro comando.",
                ephemeral=True
            )
            return
        
        if interaction.user.id not in (sender_id, target_id):
            return await interaction.response.send_message(
                f"{emoji('error')} Ei, {interaction.user.mention}. Esse pagamento não pertence a você. Cai fora!",
                ephemeral=True
            )


        if key not in self.accepted:
            self.accepted[key] = {
                "sender": False,
                "target": False
            }

        pay = self.accepted[key]

        if interaction.user.id == sender_id:
            if pay["sender"]:
                return await interaction.response.send_message(
                    f"{emoji('error')} Você já confirmou este pagamento.",
                    ephemeral=True
                )

            pay["sender"] = True

        elif interaction.user.id == target_id:
            if pay["target"]:
                return await interaction.response.send_message(
                    f"{emoji('error')} Você já confirmou este pagamento.",
                    ephemeral=True
                )

            pay["target"] = True

        accepted = int(pay["sender"]) + int(pay["target"])

        if accepted < 2:
            button = discord.ui.Button(
                label=f"Transferir ({accepted}/2)",
                style=discord.ButtonStyle.success,
                custom_id=custom_id,
                emoji=emoji("check")
            )

            cancel = discord.ui.Button(
                label="Cancelar",
                style=discord.ButtonStyle.danger,
                custom_id=f"pay_cancel_{sender_id}_{target_id}_{amount}",
                emoji=emoji("error")
            )

            support = discord.ui.Button(
                label="Suporte",
                style=discord.ButtonStyle.link,
                url="https://discord.gg/CUv9QAxJPa"
            )

            view = discord.ui.LayoutView(timeout=None)

            target = self.bot.get_user(target_id)
            user = self.bot.get_user(sender_id)

            view.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('money')} Pagamento iniciado\n"
                    f"> {target.mention}, {user.mention} deseja transferir **[ `{amount}` | `{abv(amount)}` ] {emoji('ducos')} Ducos** para você.\n"
                    f"{emoji('info')} Para que a transferência seja concluída, ambos os usuários precisam confirmar o pagamento.\n"
                    f"-# ⤷ O pedido permanecerá disponível por até 15 minutos antes de ser cancelado automaticamente.\n\n"
                    f"> Após a confirmação, os Ducos serão transferidos imediatamente para a conta do destinatário sem necessidade de etapas adicionais."
                )
            )
            
            view.add_item(
                discord.ui.ActionRow(
                    button,
                    cancel,
                    support
                )
            )

            return await interaction.response.edit_message(
                view=view
            )

        self.accepted.pop(key, None)

        await add(target_id, "money", amount)
        await sub(sender_id, "money", amount)
        await setV(sender_id, "in_pay", False)

        await interaction.response.edit_message(
            view=InteractionMessage(
                amount,
                sender,
                target
            )
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(
        PayAcceptInteraction(bot)
    )
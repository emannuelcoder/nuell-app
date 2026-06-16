import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from src.database.repositories.user_repository import get, setV
from src.utils.abbreviate import abv
from src.utils.parse import parse

class PayMessage(discord.ui.LayoutView):
    def __init__(
        self,
        bot: commands.Bot,
        user: discord.User,
        target: discord.User,
        amount: str,
        inPay: bool,
        userMoney: int
    ):
        super().__init__(timeout=900)

        self.bot = bot
        self.user = user
        self.target = target
        self.message = None
        self.valid = False

        supportButton = discord.ui.Button(
            label="Suporte",
            style=discord.ButtonStyle.link,
            url="https://discord.gg/support"
        )

        try:
            self.amount = parse(amount)
        except ValueError:
            self.amount = None

        if inPay:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('error')} Erro no pagamento\n"
                    f"> {user.mention}, você já possui um pagamento pendente no momento e não pode iniciar outro agora.\n"
                    f"{emoji('info')} Aguarde o pagamento atual ser concluído ou cancele-o antes de tentar criar uma nova transferência.\n"
                    f"-# ⤷ {emoji('warning')} Caso nenhuma ação seja realizada, o pagamento será cancelado automaticamente após 15 minutos.\n\n"
                    f"> Se acreditar que houve algum erro, entre em contato com nossa equipe através do suporte."
                )
            )

            self.add_item(
                discord.ui.ActionRow(
                    supportButton
                )
            )

            return

        if user.id == target.id:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('error')} Erro no pagamento\n"
                    f"> {user.mention}, você tentou transferir Ducos para sua própria conta, mas isso não é permitido.\n"
                    f"{emoji('info')} Escolha outro usuário para receber os Ducos e tente novamente.\n\n"
                    f"> Se acreditar que houve algum erro, entre em contato com nossa equipe através do suporte."
                )
            )

            self.add_item(
                discord.ui.ActionRow(
                    supportButton
                )
            )

            return

        if self.amount is None or self.amount <= 0:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('error')} Erro no pagamento\n"
                    f"> {user.mention}, o valor informado não é válido para uma transferência.\n"
                    f"{emoji('info')} Você pode utilizar números normais ou abreviações para informar a quantia desejada.\n"
                    f"-# ⤷ Exemplos válidos: 1000, 10k, 500k, 1kk, 1m ou 2.5m.\n\n"
                    f"> Confira o valor digitado e tente novamente utilizando um formato válido."
                    f"> Se acreditar que houve algum erro, entre em contato com nossa equipe através do suporte."
                )
            )

            self.add_item(
                discord.ui.ActionRow(
                    supportButton
                )
            )

            return

        if userMoney < self.amount:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('error')} Erro no pagamento\n"
                    f"> {user.mention}, você não possui **{emoji('ducos')} Ducos** suficientes para enviar essa quantia.\n"
                    f"{emoji('info')} Verifique seu saldo atual e tente novamente com um valor menor caso necessário.\n"
                    f"-# ⤷ Utilize o comando </saldo:1513679777410846854> para visualizar seu saldo completo.\n\n"
                    f"> Se acreditar que houve algum erro, entre em contato com nossa equipe através do suporte."
                )
            )

            self.add_item(
                discord.ui.ActionRow(
                    supportButton
                )
            )

            return
        
        if target.bot:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('error')} Erro no pagamento\n"
                    f"> {user.mention}, você não pode transferir **{emoji('ducos')} Ducos** para um bot!\n"
                    f"{emoji('info')} Verifique se enviou-me o destinatário corretamente.\n"
                    f"-# ⤷ Você só pode transferir**Ducos** para um ser humano.\n\n"
                    f"> Se acreditar que houve algum erro, entre em contato com nossa equipe através do suporte."
                )
            )

            self.add_item(
                discord.ui.ActionRow(
                    supportButton
                )
            )

            return

        self.valid = True

        acceptButton = discord.ui.Button(
            label="Transferir (0/2)",
            style=discord.ButtonStyle.success,
            custom_id=f"pay_accept_{user.id}_{target.id}_{self.amount}",
            emoji=emoji("check")
        )
        cancelButton = discord.ui.Button(
            label="Cancelar",
            style=discord.ButtonStyle.danger,
            custom_id=f"pay_cancel_{user.id}_{target.id}_{self.amount}",
            emoji=emoji("error")
        )

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('money')} Pagamento iniciado\n"
                f"> {target.mention}, {user.mention} deseja transferir **[ `{self.amount}` | `{abv(self.amount)}` ] {emoji('ducos')} Ducos** para você.\n"
                f"{emoji('info')} Para que a transferência seja concluída, ambos os usuários precisam confirmar o pagamento.\n"
                f"-# ⤷ O pedido permanecerá disponível por até 15 minutos até os botões serem desabilitados.\n\n"
                f"> Após a confirmação, os **Ducos** serão transferidos imediatamente para a conta do destinatário sem necessidade de etapas adicionais."
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                acceptButton,
                cancelButton,
                supportButton
            )
        )

    async def on_timeout(self):
        for item in self.children:
            try:
                item.disabled = True
            except:
                pass

        try:
            await self.message.edit(view=self)
        except:
            pass

        await setV(self.user.id, "in_pay", False)

class Pay(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="transferir",
        description="Transfira Ducos para outro usuário."
    )

    @app_commands.describe(
        usuário="Usuário que os Ducos serão transferidos.",
        quantia="Quantidade de Ducos a ser transferidos."
    )

    async def pay(
        self,
        interaction: discord.Interaction,
        usuário: discord.User,
        quantia: str
    ):
        user = interaction.user

        userMoney = await get(user.id, "money")
        inPay = await get(user.id, "in_pay")

        view = PayMessage(
            self.bot,
            user,
            usuário,
            quantia,
            inPay,
            userMoney
        )

        await interaction.response.send_message(
            view=view
        )

        try:
            view.message = await interaction.original_response()
        except:
            pass

        if view.valid:
            await setV(user.id, "in_pay", True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Pay(bot))
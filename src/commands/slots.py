import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from src.utils.abbreviate import abv
from src.utils.parse import parse
from src.database.repositories.user_repository import setV, get

class SlotsMessage(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot, user: discord.User, amount: str, inBet: bool, userMoney: int, timeout = 900):
        super().__init__(timeout=timeout)

        self.bot = bot
        self.user = user
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

        if inBet:
            self.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('error')} Erro ao apostar\n"
                    f"> {user.mention}, você já possui uma aposta ativa no momento e não pode iniciar outra agora.\n"
                    f"{emoji('info')} Aguarde a aposta pendente ser concluída ou cancele-a antes de tentar iniciar uma nova aposta.\n"
                    f"-# ⤷ {emoji('warning')} Caso nenhuma ação seja realizada, a aposta será cancelada automaticamente após 15 minutos.\n\n"
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
                    f"## {emoji('error')} Erro ao apostar\n"
                    f"> {user.mention}, o valor informado não é válido para apostar.\n"
                    f"{emoji('info')} Você pode utilizar números normais ou abreviações para informar a quantia desejada.\n"
                    f"-# ⤷ Exemplos válidos: 1000, 10k, 500k, 1kk, 1m ou 2.5m.\n\n"
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
                    f"## {emoji('error')} Erro ao apostar\n"
                    f"> {user.mention}, você não possui **{emoji('ducos')} Ducos** suficientes para apostar.\n"
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

        self.valid = True

        initBet = discord.ui.Button(
            label="Iniciar Aposta",
            style=discord.ButtonStyle.success,
            custom_id=f"slots_play_{user.id}_{amount}",
            emoji=emoji("check")
        )
        cancelBet = discord.ui.Button(
            label="Cancelar",
            style=discord.ButtonStyle.danger,
            custom_id=f"slots_cancel_{user.id}_{amount}",
            emoji=emoji("error")
        )

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('slots')} Iniciar a aposta\n"
                f"> {user.mention}, você realmente deseja apostar **[ `{self.amount}` | `{abv(self.amount)}` ] {emoji('ducos')} Ducos**?\n"
                f"{emoji('info')} Para que a aposta seja iniciada, você deverá apertar no botão \"Iniciar Aposta\".\n"
                f"-# ⤷ Você tem 15 minutos para iniciar a aposta, após esse tempo passar, os botões serão desabilitados.\n\n"
                f"> Lembre-se: caso você perca a aposta, seu **Ducos** não serão devolvidos."
            )
        )

        self.add_item(
            discord.ui.ActionRow(
                initBet,
                cancelBet,
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

        await setV(self.user.id, "in_bet", False)

class Slots(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="slots",
        description="Aposte ducos na máquina de slots."
    )

    @app_commands.describe(
        quantia="Quantia de Ducos a ser apostada."
    )

    async def slots(
        self,
        interaction: discord.Interaction,
        quantia: str
    ):
        user = interaction.user

        userMoney = await get(user.id, "money")
        inBet = await get(user.id, "in_bet")

        view = SlotsMessage(
            self.bot,
            user,
            quantia,
            inBet,
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
            await setV(user.id, "in_bet", True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Slots(bot))

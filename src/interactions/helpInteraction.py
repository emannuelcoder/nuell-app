import discord
from discord.ext import commands
from src.utils.emojis import emoji

class Container(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)

        container = discord.ui.Container(
            accent_color=discord.Color.blue()
        )

        values = interaction.data.get("values")
        if not values:
            return

        value = values[0]

        if value == "mod":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('moderacao')} Comandos de Moderação\n"
                    f"### </banir:1515858792279965798>\n⤷ Bana um usuário do servidor.\n"
                    f"### </desbanir:1515864849668640839>\n⤷ Desbana um usuário do servidor.\n"
                    f"### </mute:1515875247486931067>\n⤷ Silencie um usuário do servidor.\n"
                    f"### </unmute:1515875247486931068>\n⤷ Dessilencie um usuário do servidor.\n"
                    f"### </trancar canal:1515878796522426552>\n⤷ Tranque um canal do servidor.\n"
                    f"### </destrancar canal:1515878796522426553>\n⤷ Destranque um canal do servidor."
                )
            )

        elif value == "eco":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('money')} Comandos de Economia\n"
                    f"### </diário:1513679777410846855>\n⤷ Resgate sua recompensa diária de **Ducos**.\n"
                    f"### </saldo:1513679777410846854>\n⤷ Consulte o saldo de **Ducos** de alguém.\n"
                    f"### </transferir:1513679777410846858>\n⤷ Transfira **Ducos** a um usuário.\n"
                    f"### </trabalhar:1513679777410846860>\n⤷ Trabalhe para ganhar **Ducos**.\n"
                    f"### </slots:1514638107218153653>\n⤷ Aposte **Ducos** na máquina de caça-níqueis."
                )
            )

        elif value == "fun":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('confetes')} Comandos para Diversão\n"
                    f"### </8ball:1516566662432686202>\n⤷ Receba uma resposta aleatória.\n"
                    f"### </piadas:1516572751224115292>\n⤷ Receba uma piada aleatória.\n"
                    f"### </beijar:1516585155307765892>\n⤷ Beije um usuário.\n"
                    f"### </abraçar:1516583019056730302>\n⤷ Abrace um usuário."
                )
            )

        elif value == "util":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('info')} Comandos Utilitários\n"
                    f"### </usuário info:1514620101444374700>\n⤷ Veja as informações de um usuário.\n"
                    f"### </servidor info:1515003250737414327>\n⤷ Veja as informações do servidor.\n"
                    f"### </nuell info:1513723574345662464>\n⤷ Veja minhas informações.\n"
                    f"### </falar:1513696698277302333>\n⤷ Envie uma mensagem através bot."
                )
            )

        elif value == "ai":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('gpt')} Comandos de Inteligência Artificial\n"
                    f"### </chat:1516449051812434061>\n⤷ Converse com a **IA do Nuell**.\n"
                )
            )

        self.add_item(container)

class HelpInteraction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        if interaction.type != discord.InteractionType.component:
            return

        if not interaction.data:
            return

        if interaction.data.get("custom_id") != "help_menu":
            return

        await interaction.response.send_message(
            view=Container(interaction),
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpInteraction(bot))
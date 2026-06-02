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
                    f"### /ban\n⤷ Bana um usuário do servidor.\n"
                    f"### /unban\n⤷ Desbana um usuário do servidor.\n"
                    f"### /mute\n⤷ Silencie um usuário do servidor.\n"
                    f"### /unmute\n⤷ Dessilencie um usuário do servidor.\n"
                    f"### /lock\n⤷ Tranque um canal do servidor.\n"
                    f"### /unlock\n⤷ Destranque um canal do servidor."
                )
            )

        elif value == "eco":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('money')} Comandos de Economia\n"
                    f"### /daily\n⤷ Resgate sua recompensa diária.\n"
                    f"### /pay\n⤷ Pague um usuário.\n"
                    f"### /work\n⤷ Trabalhe para ganhar dinheiro.\n"
                    f"### /bet\n⤷ Aposte dinheiro."
                )
            )

        elif value == "fun":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('confetes')} Comandos para Diversão\n"
                    f"### /8ball\n⤷ Receba uma resposta aleatória.\n"
                    f"### /meme\n⤷ Envia um meme aleatório.\n"
                    f"### /joke\n⤷ Envia uma piada aleatória.\n"
                    f"### /kiss\n⤷ Beije um usuário.\n"
                    f"### /hug\n⤷ Abrace um usuário.\n"
                    f"### /gay\n⤷ Veja o quanto gay um usuário é."
                )
            )

        elif value == "util":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('info')} Comandos Utilitários\n"
                    f"### /user info\n⤷ Veja as informações de um usuário.\n"
                    f"### /server info\n⤷ Veja as informações do servidor.\n"
                    f"### /bot info\n⤷ Veja minhas informações.\n"
                    f"### /isbot\n⤷ Veja se um usuário é um bot.\n"
                    f"### /say\n⤷ Envie uma mensagem pelo bot.\n"
                    f"### /premium\n⤷ Veja seu status premium."
                )
            )

        elif value == "ai":
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('gpt')} Comandos de Inteligência Artificial\n"
                    f"### /chat\n⤷ Converse com uma IA.\n"
                    f"### /image gen\n⤷ Gere imagens usando IA."
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
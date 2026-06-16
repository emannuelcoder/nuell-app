import re
import discord
from datetime import timedelta
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji

def parse_tempo(tempo: str):
    match = re.fullmatch(r"(\d+)(s|m|h|d)", tempo.lower())

    if not match:
        return None

    valor = int(match.group(1))
    unidade = match.group(2)

    if valor <= 0:
        return None

    if unidade == "s":
        return timedelta(seconds=valor)

    if unidade == "m":
        return timedelta(minutes=valor)

    if unidade == "h":
        return timedelta(hours=valor)

    if unidade == "d":
        return timedelta(days=valor)

class MuteMessage(discord.ui.LayoutView):
    def __init__(
        self,
        author: discord.Member,
        muted: discord.Member,
        tempo: str,
        reason: str
    ):
        super().__init__()

        self.add_item(
            discord.ui.TextDisplay(
                f"# {emoji('martelo')} Tribunal\n"
                f"> O **Staff** {author.mention} **silenciou** o **usuário** {muted.mention}.\n"
                f"- Tempo: **{tempo}**\n"
                f"- Motivo: **{reason}**"
            )
        )

class ErrorMessage(discord.ui.LayoutView):
    def __init__(self, message: str):
        super().__init__()

        self.add_item(
            discord.ui.TextDisplay(
                f"# {emoji('tribunal')} Tribunal\n"
                f"> {emoji('error')} {message}"
            )
        )

class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="mute",
        description="Silencie um usuário"
    )

    @app_commands.describe(
        usuário="Usuário a ser silenciado",
        tempo="Tempo do silenciamento. Ex.: 10d, 10h, 10m ou 10s",
        motivo="Motivo do silenciamento."
    )

    async def mute(
        self,
        interaction: discord.Interaction,
        usuário: discord.Member,
        tempo: str,
        motivo: str = "Nenhum motivo especificado."
    ):
        guild = interaction.guild
        author = interaction.user
        me = guild.me

        if not author.guild_permissions.moderate_members:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não possui permissão para **silenciar membros**."
                ),
                ephemeral=True
            )

        if not me.guild_permissions.moderate_members:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Eu não possuo permissão para **silenciar membros**."
                ),
                ephemeral=True
            )

        if usuário == author:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode silenciar a **si mesmo**."
                ),
                ephemeral=True
            )

        if usuário == guild.owner:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode silenciar o **dono do servidor**."
                ),
                ephemeral=True
            )

        if usuário.guild_permissions.administrator:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode silenciar um **administrador**."
                ),
                ephemeral=True
            )

        if usuário.top_role >= author.top_role and author != guild.owner:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode silenciar alguém que possui um cargo **igual ou superior** ao seu."
                ),
                ephemeral=True
            )

        if usuário.top_role >= me.top_role:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Não consigo silenciar este usuário porque o cargo dele é **igual ou superior** ao meu."
                ),
                ephemeral=True
            )

        duração = parse_tempo(tempo)

        if duração is None:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Tempo inválido.\n"
                    f"- Exemplos: **30s**, **5m**, **2h**, **1d**, **28d**."
                ),
                ephemeral=True
            )

        if duração > timedelta(days=28):
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "O tempo máximo é de **28 dias**."
                ),
                ephemeral=True
            )

        if usuário.is_timed_out():
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Este usuário **já está silenciado**."
                ),
                ephemeral=True
            )

        try:
            await usuário.timeout(
                duração,
                reason=f"{motivo} | Por {author}"
            )

            await interaction.response.send_message(
                view=MuteMessage(
                    author,
                    usuário,
                    tempo,
                    motivo
                )
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Não tenho permissão para silenciar este usuário."
                ),
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Ocorreu um erro ao silenciar o usuário.\n- Erro: `{e}`"
                ),
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Mute(bot))
import discord
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji

class UnmuteMessage(discord.ui.LayoutView):
    def __init__(
        self,
        author: discord.Member,
        unmuted: discord.Member,
        reason: str
    ):
        super().__init__()

        self.add_item(
            discord.ui.TextDisplay(
                f"# {emoji('martelo')} Tribunal\n"
                f"> O **Staff** {author.mention} **dessilenciou** o **usuário** {unmuted.mention}.\n"
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

class Unmute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="unmute",
        description="Dessilencie um usuário"
    )

    @app_commands.describe(
        usuário="Usuário a ser dessilenciado",
        motivo="Motivo do dessilenciamento."
    )

    async def unmute(
        self,
        interaction: discord.Interaction,
        usuário: discord.Member,
        motivo: str = "Nenhum motivo especificado."
    ):
        guild = interaction.guild
        author = interaction.user
        me = guild.me

        if not author.guild_permissions.moderate_members:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não possui permissão para **dessilenciar membros**."
                ),
                ephemeral=True
            )

        if not me.guild_permissions.moderate_members:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Eu não possuo permissão para **dessilenciar membros**."
                ),
                ephemeral=True
            )

        if usuário == guild.owner:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode dessilenciar o **dono do servidor**."
                ),
                ephemeral=True
            )

        if usuário.guild_permissions.administrator:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Este usuário é um **administrador**."
                ),
                ephemeral=True
            )

        if usuário.top_role >= author.top_role and author != guild.owner:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode dessilenciar alguém que possui um cargo **igual ou superior** ao seu."
                ),
                ephemeral=True
            )

        if usuário.top_role >= me.top_role:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Não consigo dessilenciar este usuário porque o cargo dele é **igual ou superior** ao meu."
                ),
                ephemeral=True
            )

        if not usuário.is_timed_out():
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Este usuário **não está silenciado**."
                ),
                ephemeral=True
            )

        try:
            await usuário.timeout(
                None,
                reason=f"{motivo} | Por {author}"
            )

            await interaction.response.send_message(
                view=UnmuteMessage(
                    author,
                    usuário,
                    motivo
                )
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Não tenho permissão para dessilenciar este usuário."
                ),
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Ocorreu um erro ao dessilenciar o usuário.\n- Erro: `{e}`"
                ),
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Unmute(bot))
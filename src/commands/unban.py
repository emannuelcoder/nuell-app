import discord
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji

class UnbanMessage(discord.ui.LayoutView):
    def __init__(
        self,
        author: discord.Member,
        user: discord.User,
        reason: str
    ):
        super().__init__()

        self.add_item(
            discord.ui.TextDisplay(
                f"# {emoji('martelo')} Tribunal\n"
                f"> O **Staff** {author.mention} **desbaniu** o **usuário** {user.mention}.\n"
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

class Unban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="desbanir",
        description="Desbane um usuário"
    )

    @app_commands.describe(
        usuário_id="ID do usuário a ser desbanido",
        motivo="Motivo do desbanimento."
    )

    async def unban(
        self,
        interaction: discord.Interaction,
        usuário_id: str,
        motivo: str = "Nenhum motivo especificado."
    ):
        guild = interaction.guild
        author = interaction.user
        me = guild.me

        if not author.guild_permissions.ban_members:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não possui permissão para **banir membros**."
                ),
                ephemeral=True
            )

        if not me.guild_permissions.ban_members:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Eu não possuo permissão para **banir membros**."
                ),
                ephemeral=True
            )

        try:
            usuário_id = int(usuário_id)

        except ValueError:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "O **ID informado é inválido**."
                ),
                ephemeral=True
            )

        try:
            usuário = await self.bot.fetch_user(usuário_id)

        except discord.NotFound:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Não encontrei um usuário com este **ID**."
                ),
                ephemeral=True
            )

        try:
            await guild.fetch_ban(usuário)

        except discord.NotFound:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Este usuário **não está banido**."
                ),
                ephemeral=True
            )

        try:
            await guild.unban(
                usuário,
                reason=f"{motivo} | Por {author}"
            )

            await interaction.response.send_message(
                view=UnbanMessage(
                    author,
                    usuário,
                    motivo
                )
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Não tenho permissão para **desbanir** este usuário."
                ),
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Ocorreu um erro ao desbanir o usuário.\n- Erro: `{e}`"
                ),
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Unban(bot))
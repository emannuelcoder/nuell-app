import discord
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji

class BanMessage(discord.ui.LayoutView):
    def __init__(
        self,
        author: discord.Member,
        banned: discord.Member,
        reason: str
    ):
        super().__init__()

        self.add_item(
            discord.ui.TextDisplay(
                f"# {emoji('martelo')} Tribunal\n"
                f"> O **Staff** {author.mention} **baniu** o **usuário** {banned.mention}.\n"
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

class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="banir",
        description="Bane um usuário"
    )

    @app_commands.describe(
        usuário="Usuário a ser banido",
        motivo="Motivo do banimento."
    )

    async def ban(
        self,
        interaction: discord.Interaction,
        usuário: discord.Member,
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

        if usuário == author:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode banir a **si mesmo**."
                ),
                ephemeral=True
            )

        if usuário == guild.owner:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode banir o **dono do servidor**."
                ),
                ephemeral=True
            )

        if usuário.top_role >= author.top_role and author != guild.owner:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não pode banir alguém que possui um cargo **igual ou superior** ao seu."
                ),
                ephemeral=True
            )

        if usuário.top_role >= me.top_role:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Não consigo banir este usuário porque o cargo dele é **igual ou superior** ao meu."
                ),
                ephemeral=True
            )

        try:
            await usuário.ban(reason=f"{motivo} | Por {author}")

            await interaction.response.send_message(
                view=BanMessage(
                    author,
                    usuário,
                    motivo
                )
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Não tenho permissão para banir este usuário."
                ),
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Ocorreu um erro ao banir o usuário.\n- Erro: `{e}`"
                ),
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Ban(bot))
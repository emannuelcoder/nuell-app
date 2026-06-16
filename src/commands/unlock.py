import discord
from discord import app_commands
from discord.ext import commands
from src.utils.emojis import emoji

class LockMessage(discord.ui.LayoutView):
    def __init__(
        self,
        author: discord.Member,
        channel: discord.TextChannel,
        reason: str
    ):
        super().__init__()

        self.add_item(
            discord.ui.TextDisplay(
                f"# {emoji('martelo')} Tribunal\n"
                f"> O **Staff** {author.mention} **destrancou** o canal {channel.mention}.\n"
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

class Lock(commands.GroupCog, name="destrancar"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="canal",
        description="Destranque um canal"
    )

    @app_commands.describe(
        canal="Canal a ser destrancado.",
        motivo="Motivo do destrancamento."
    )

    async def lock(
        self,
        interaction: discord.Interaction,
        canal: discord.TextChannel | None = None,
        motivo: str = "Nenhum motivo especificado."
    ):
        guild = interaction.guild
        channel = canal or interaction.channel

        author = interaction.user
        me = guild.me

        if not author.guild_permissions.manage_channels:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Você não possui permissão para **gerenciar canais**."
                ),
                ephemeral=True
            )

        if not me.guild_permissions.manage_channels:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Eu não possuo permissão para **gerenciar canais**."
                ),
                ephemeral=True
            )

        everyone = guild.default_role

        overwrite = channel.overwrites_for(everyone)

        if overwrite.send_messages is True:
            return await interaction.response.send_message(
                view=ErrorMessage(
                    "Este canal **já está destrancado**."
                ),
                ephemeral=True
            )

        try:
            overwrite.send_messages = True

            await channel.set_permissions(
                everyone,
                overwrite=overwrite,
                reason=f"{motivo} | Por {author}"
            )

            await interaction.response.send_message(
                view=LockMessage(
                    author,
                    channel,
                    motivo
                )
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Não tenho permissão para destrancar este canal."
                ),
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                view=ErrorMessage(
                    "Ocorreu um erro ao destrancar o canal.\n- Erro: `{e}`"
                ),
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Lock(bot))
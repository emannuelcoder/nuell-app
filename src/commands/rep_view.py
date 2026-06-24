import discord
from discord.ext import commands
from discord import app_commands
from src.database.repositories.user_repository import get_or_create_user
from src.utils.emojis import emoji
from src.utils.cooldown import check

class Message(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction, user: discord.User, reps: int):
        super().__init__()
        self.user = user
        self.reps = reps

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('like')} Reputações de {user.mention}\n"
            )
        )

        if interaction.user.id != user.id:
            self.add_item(
                discord.ui.TextDisplay(
                    f"{interaction.user.mention}, atualmente tem {user.mention} é **[ `{reps}` ] reputações**."
                )
            )
        else:
            self.add_item(
                discord.ui.TextDisplay(
                    f"{interaction.user.mention}, atualmente você tem **[ `{reps}` ] reputações**."
                )
            )


class RepsView(commands.GroupCog, name="reputações"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ver",
        description="Veja suas reputações ou de outro usuário."
    )

    @app_commands.describe(
        usuário="Veja as reputações de outro usuário."
    )

    async def saldo(
        self,
        interaction: discord.Interaction,
        usuário: discord.User | None = None
    ):
        can_use, remaining = await check(interaction.user.id)

        if not can_use:
            await interaction.response.send_message(
                f"{emoji('time')} Aguarde **{remaining}s** antes de usar outro comando.",
                ephemeral=True
            )
            return
        
        target_user = usuário or interaction.user

        db_user = await get_or_create_user(target_user.id)

        await interaction.response.send_message(
            view=Message(
                interaction,
                target_user,
                db_user.reps
            )
        )

async def setup(bot):
    await bot.add_cog(RepsView(bot))
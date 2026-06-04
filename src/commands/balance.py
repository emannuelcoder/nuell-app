import discord
from discord.ext import commands
from discord import app_commands
from src.database.repositories.user_repository import get_or_create_user
from src.utils.emojis import emoji
from src.utils.abbreviate import abv

class Message(discord.ui.LayoutView):
    def __init__(self, interaction: discord.Interaction, user: discord.User, balance: int):
        super().__init__(timeout=None)
        self.user = user
        self.balance = balance

        self.add_item(
            discord.ui.TextDisplay(
                f"## Saldo de {user.mention}\n"
            )
        )

        if interaction.user.id != user.id:
            self.add_item(
                discord.ui.TextDisplay(
                    f"{interaction.user.mention}, o saldo atual de {user.mention} é **[ `{balance}` | `{abv(balance)}` ] {emoji('ducos')} Ducos.**"
                )
            )
        else:
            self.add_item(
                discord.ui.TextDisplay(
                    f"{interaction.user.mention}, seu saldo atual é **[ `{balance}` | `{abv(balance)}` ] {emoji('ducos')} Ducos.**"
                )
            )


class Balance(commands.GroupCog, name="ducos"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="atm", description="Veja o seu saldo de Ducos ou de outro usuário.")
    async def saldo(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None
    ):
        target_user = user or interaction.user

        db_user = await get_or_create_user(target_user.id)

        await interaction.response.send_message(
            view=Message(
                interaction,
                target_user,
                db_user.money
            )
        )

async def setup(bot):
    await bot.add_cog(Balance(bot))
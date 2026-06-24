import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from src.database.repositories.user_repository import setV, get
from src.utils.cooldown import check

class Message(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot, author: discord.User, target: discord.Member):
        super().__init__()

        self.bot = bot
        self.author = author
        self.target = target

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('like')} Enviar reputação\n"
                f"> {self.author.mention}, você está prestes a enviar **1 reputação** para {self.target.mention}.\n"
                f"-# {emoji('info')} Para enviar a reputação, aperte o botão abaixo."
            )
        )

        sendRep = discord.ui.Button(
            label="Enviar Reputação",
            style=discord.ButtonStyle.primary,
            emoji=emoji('like'),
            custom_id=f"sendrep_{self.author.id}_{self.target.id}"
        )

        self.add_item(
            discord.ui.ActionRow(sendRep)
        )

class SendRep(commands.GroupCog, name="enviar"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="reputação",
        description="Envie uma reputação para um usuário"
    )

    @app_commands.describe(
        usuário="Usuário a quem a reputação será enviada"
    )

    async def sendrep(self, interaction: discord.Interaction, usuário: discord.Member):
        can_use, remaining = await check(interaction.user.id)

        if not can_use:
            await interaction.response.send_message(
                f"{emoji('time')} Aguarde **{remaining}s** antes de usar outro comando.",
                ephemeral=True
            )
            return
        
        if usuário.id == interaction.user.id:
            await interaction.response.send_message(
                content=f"{emoji('error')} Você não pode enviar reputações para você mesmo!", ephemeral=True
            )
        
        await interaction.response.send_message(
            view=Message(self.bot, interaction.user, usuário)
        )

async def setup(bot):
    await bot.add_cog(SendRep(bot))
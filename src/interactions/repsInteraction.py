import discord
from discord.ext import commands
from src.utils.emojis import emoji
from src.database.repositories.user_repository import setV, get

class NewMessage(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot, author: discord.User, target: discord.Member, totalReps: int):
        super().__init__()

        self.bot = bot
        self.author = author
        self.target = target

        self.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('like')} Reputação enviada\n"
                f"> {self.author.mention}, você acabou de enviar **1 reputação** para {self.target.mention}.\n"
                f"-# {emoji('info')} Agora {self.target.mention} possuí **{totalReps} reputações**."
            )
        )

        sendRep = discord.ui.Button(
            label="Enviar Reputação",
            style=discord.ButtonStyle.primary,
            emoji=emoji('like'),
            custom_id="sendrep",
            disabled=True
        )

        self.add_item(discord.ui.ActionRow(sendRep))

class RepInteraction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(
        self,
        interaction: discord.Interaction
    ):

        if interaction.type != discord.InteractionType.component:
            return

        custom_id = interaction.data.get("custom_id")

        if not custom_id:
            return

        if not custom_id.startswith("sendrep_"):
            return

        _, author_id, target_id = custom_id.split("_")

        author_id = int(author_id)
        target_id = int(target_id)

        if interaction.user.id != author_id:
            return await interaction.response.send_message(
                f"{emoji('error')} Apenas quem iniciou o envio pode confirmar a reputação.",
                ephemeral=True
            )

        target = interaction.guild.get_member(target_id)

        if not target:
            return await interaction.response.send_message(
                f"{emoji('error')} Não foi possível encontrar esse usuário.",
                ephemeral=True
            )

        now = int(discord.utils.utcnow().timestamp())

        cd_reps = await get(
            interaction.user.id,
            "reps_cd"
        )

        if cd_reps and cd_reps > now:

            view = discord.ui.LayoutView()

            view.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('like')} Reputação\n"
                    f"> {emoji('error')} {interaction.user.mention}, você enviou uma reputação recentemente.\n"
                    f"> {emoji('time')} Você poderá enviar outra em **[ <t:{cd_reps}:t> | <t:{cd_reps}:R> ]**."
                )
            )

            return await interaction.response.send_message(
                view=view,
                ephemeral=True
            )

        cooldown = now + 10800

        await setV(
            interaction.user.id,
            "reps_cd",
            cooldown
        )

        reps = await get(
            target.id,
            "reps"
        )

        await setV(
            target.id,
            "reps",
            reps + 1
        )

        totalReps = reps + 1

        await interaction.response.edit_message(
            view=NewMessage(
                self.bot,
                interaction.user,
                target,
                totalReps
            )
        )

        await interaction.response.send_message(
            content=f"{emoji('check')} Reputação enviada!", ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(
        RepInteraction(bot)
    )
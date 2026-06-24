import discord
from discord.ext import commands
from discord import app_commands
from src.utils.cooldown import check
from src.utils.emojis import emoji


class ServerInfoView(discord.ui.LayoutView):
    def __init__(
        self,
        bot: commands.Bot,
        guild: discord.Guild,
        author: discord.User,
        timeout: int = 600
    ):
        super().__init__(timeout=timeout)

        self.bot = bot
        self.guild = guild
        self.author = author

        self.page = 1
        self.max_pages = 3

        self.render()

    def render(self):
        self.clear_items()

        guild = self.guild

        created = int(guild.created_at.timestamp())

        members = guild.member_count or 0
        bots = sum(1 for member in guild.members if member.bot)
        humans = members - bots

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        total_channels = len(guild.channels) - 1

        roles = len(guild.roles) - 1
        highest_role = max(
            guild.roles,
            key=lambda role: role.position
        )

        emojis_count = len(guild.emojis)
        animated_emojis = sum(
            1 for e in guild.emojis if e.animated
        )

        verification_levels = {
            discord.VerificationLevel.none: "Nenhum",
            discord.VerificationLevel.low: "Baixo",
            discord.VerificationLevel.medium: "Médio",
            discord.VerificationLevel.high: "Alto",
            discord.VerificationLevel.highest: "Muito Alto"
        }

        verification = verification_levels.get(
            guild.verification_level,
            "Desconhecido"
        )

        boost_level = guild.premium_tier
        boosts = guild.premium_subscription_count or 0

        owner = guild.owner

        description = guild.description or "Nenhuma descrição."

        container = discord.ui.Container(
            accent_color=discord.Color.blue()
        )

        if self.page == 1:
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('info')} Informações do Servidor\n"
                    f"### {emoji('prancheta')} Informações básicas\n"
                    f"> Nome: **{guild.name}**\n"
                    f"> ID: **{guild.id}**\n"
                    f"> Dono: {owner.mention if owner else 'Desconhecido'}\n"
                    f"> Criado em:\n"
                    f"> - <t:{created}:F>\n"
                    f"> - <t:{created}:R>\n"
                    f"> Nível de verificação: **{verification}**"
                )
            )

        elif self.page == 2:
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('info')} Membros e Canais\n"
                    f"### {emoji('user')} Membros\n"
                    f"> Total: **{members:,}**\n"
                    f"> Humanos: **{humans:,}**\n"
                    f"> Bots: **{bots:,}**\n"
                    f"### {emoji('text')} Canais\n"
                    f"> Total: **{total_channels}**\n"
                    f"> Texto: **{text_channels}**\n"
                    f"> Voz: **{voice_channels}**\n"
                    f"### {emoji('role')} Cargos\n"
                    f"> Total: **{roles}**\n"
                    f"> Mais alto: **{highest_role.mention}**"
                )
            )

        elif self.page == 3:
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('info')} Extras\n"
                    f"### {emoji('rocket')} Boosts\n"
                    f"> Nível: **{boost_level}**\n"
                    f"> Quantidade: **{boosts}**\n"
                    f"### {emoji('feliz')} Emojis\n"
                    f"> Total: **{emojis_count}**\n"
                    f"> Animados: **{animated_emojis}**\n"
                    f"> Normais: **{emojis_count - animated_emojis}**\n"
                    f"### {emoji('prancheta')} Descrição\n"
                    f"> {description}"
                )
            )

            if guild.icon:
                container.add_item(
                    discord.ui.MediaGallery(
                        discord.MediaGalleryItem(
                            media=guild.icon.url
                        )
                    )
                )

            if guild.banner:
                container.add_item(
                    discord.ui.MediaGallery(
                        discord.MediaGalleryItem(
                            media=guild.banner.url
                        )
                    )
                )

        self.add_item(container)

        row = discord.ui.ActionRow()

        row.add_item(
            discord.ui.Button(
                label=" ",
                emoji=emoji("seta_esq"),
                style=discord.ButtonStyle.secondary,
                custom_id=f"server_prev_{self.author.id}",
                disabled=self.page <= 1
            )
        )

        row.add_item(
            discord.ui.Button(
                label=f"Página {self.page}/{self.max_pages}",
                style=discord.ButtonStyle.secondary,
                disabled=True
            )
        )

        row.add_item(
            discord.ui.Button(
                label=" ",
                emoji=emoji("seta_dir"),
                style=discord.ButtonStyle.secondary,
                custom_id=f"server_next_{self.author.id}",
                disabled=self.page >= self.max_pages
            )
        )

        self.add_item(row)

    async def interaction_check(
        self,
        interaction: discord.Interaction
    ) -> bool:

        custom_id = interaction.data["custom_id"]

        _, action, user_id = custom_id.split("_")

        if int(user_id) != interaction.user.id:
            await interaction.response.send_message(
                f"{emoji('error')} Você não pode usar estes botões.",
                ephemeral=True
            )
            return False

        if action == "prev":
            self.page -= 1
        elif action == "next":
            self.page += 1

        self.render()

        await interaction.response.edit_message(
            view=self
        )

        return True


class ServerInfo(
    commands.GroupCog,
    name="servidor"
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="info",
        description="Veja informações do servidor."
    )
    async def serverinfo(
        self,
        interaction: discord.Interaction
    ):
        can_use, remaining = await check(interaction.user.id)

        if not can_use:
            await interaction.response.send_message(
                f"{emoji('time')} Aguarde **{remaining}s** antes de usar outro comando.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            view=ServerInfoView(
                self.bot,
                interaction.guild,
                interaction.user
            )
        )


async def setup(bot):
    await bot.add_cog(
        ServerInfo(bot)
    )
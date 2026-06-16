import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from src.database.repositories.user_repository import get

class UserInfoView(discord.ui.LayoutView):
    def __init__(
        self,
        bot: commands.Bot,
        user: discord.Member,
        nuells: int,
        premium: bool,
        timeout: int = 600
    ):
        super().__init__(timeout=timeout)

        self.bot = bot
        self.user = user
        self.nuells = nuells
        self.premium = premium

        self.page = 1
        self.max_pages = 3

        self.render()

    def render(self):
        self.clear_items()

        user = self.user

        name = user.name
        display_name = user.display_name
        uid = user.id
        is_bot = "Sim" if user.bot else "Não"
        created = int(user.created_at.timestamp())

        container = discord.ui.Container(
            accent_color=discord.Color.blue()
        )

        if self.page == 1:
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('info')} Informações de [@{name}](<https://discord.com/users/{uid}>)\n"
                    f"### {emoji('user')} Usuário\n"
                    f"> Nome: **{name}**\n"
                    f"> Nome de exibição: **{display_name}**\n"
                    f"> ID: **{uid}**\n"
                    f"> É bot: **{is_bot}**\n"
                    f"> Conta criada:\n"
                    f"> - <t:{created}:F>\n"
                    f"> - <t:{created}:R>"
                )
            )

        elif self.page == 2:
            joined = int(user.joined_at.timestamp()) if user.joined_at else None

            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('info')} Informações de [@{name}](<https://discord.com/users/{uid}>)\n"
                    f"### {emoji('discord')} Informações do Servidor\n"
                    f"> Entrou no servidor:\n"
                    f"> <t:{joined}:F>\n"
                    f"> <t:{joined}:R>\n"
                    f"> Cargo mais alto: {user.top_role.mention}\n"
                    f"> Quantidade de cargos: **{len(user.roles) - 1}**\n"
                    f"> É booster: **{'Sim' if user.premium_since else 'Não'}**"
                )
            )

        elif self.page == 3:
            container.add_item(
                discord.ui.TextDisplay(
                    f"## {emoji('info')} Informações de [@{name}](<https://discord.com/users/{uid}>)\n"
                    f"### {emoji('alfinete')} Informações Extras\n"
                    f"> Saldo de Nuells: **{self.nuells}**\n"
                    f"> Usuário premium: **{'Sim' if self.premium else 'Não'}**"
                )
            )

        self.add_item(container)

        row = discord.ui.ActionRow()

        row.add_item(
            discord.ui.Button(
                label=" ",
                emoji=emoji("seta_esq"),
                style=discord.ButtonStyle.secondary,
                custom_id=f"userinfo_prev_{self.user.id}",
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
                custom_id=f"userinfo_next_{self.user.id}",
                disabled=self.page >= self.max_pages
            )
        )

        self.add_item(row)

    async def interaction_check(
        self,
        interaction: discord.Interaction
    ) -> bool:

        custom_id = interaction.data.get("custom_id")
        data = custom_id.split('_')

        user = int(data[2])
        action = data[1]

        if user == interaction.user.id:
            if action == "prev":
                self.page -= 1

            elif action == "next":
                self.page += 1

            self.render()

            await interaction.response.edit_message(view=self)

            return True
        else:
            await interaction.response.send_message(
                f"{emoji('error')} Erro, {interaction.user.mention}. Você não pode apertar este botão, afinal, ele não é seu. Cai fora!",
                ephemeral=True
            )

            return False
    
class UserInfo(commands.GroupCog, name="usuário"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="info",
        description="Veja as informações de um usuário"
    )

    @app_commands.describe(
        usuário="Usuário que terá suas informações exibidas"
    )

    async def userinfo(
        self,
        interaction: discord.Interaction,
        usuário: discord.Member | None = None
    ):
        user = usuário or interaction.user

        nuells = await get(user.id, "money")
        premium = await get(user.id, "premium")

        await interaction.response.send_message(
            view=UserInfoView(self.bot, user, nuells, premium)
        )

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
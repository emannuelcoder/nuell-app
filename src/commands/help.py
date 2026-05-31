import discord
from discord.ext import commands
from discord import app_commands
from src.loaders.emojis import emoji
import json

with open("secret.json", "r", encoding="utf-8") as f:
    data = json.load(f)

owner_id = data["owner_id"]


class CategoriaSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderação",
                description="Comandos voltados para moderação.",
                emoji="🛠️"
            ),
            discord.SelectOption(
                label="Economia",
                description="Comandos relacionados à economia.",
                emoji="💸"
            ),
            discord.SelectOption(
                label="Diversão",
                description="Comandos para entretenimento.",
                emoji="🎉"
            ),
            discord.SelectOption(
                label="Utilitários",
                description="Ferramentas úteis.",
                emoji="⚙️"
            ),
            discord.SelectOption(
                label="Inteligência Artificial",
                description="Comandos relacionados à IA.",
                emoji="🤖"
            ),
        ]

        super().__init__(
            placeholder="🌊 Navegue por um oceano de comandos...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Você selecionou **{self.values[0]}**.",
            ephemeral=True
        )


class AjudaView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

        self.add_item(CategoriaSelect())
        self.add_item(
            discord.ui.Button(
                label="Meu Site",
                url="https://nuell.netlify.app/",
                emoji=f"{emoji("website")}",
                row=1
            )
        )
        self.add_item(
            discord.ui.Button(
                label="Minha Comunidade",
                url="https://discord.gg/nuell",
                emoji=f"{emoji("discord")}",
                row=1
            )
        )
        self.add_item(
            discord.ui.Button(
                label="Me Adicione",
                url="https://discord.com/api/oauth2/authorize?client_id=1087444075427456000&permissions=8&scope=bot%20applications.commands",
                emoji=f"{emoji("add")}",
                row=1
            )
        )


class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajuda",
        description="Acesse a central de ajuda e comandos."
    )
    async def ajuda(self, interaction: discord.Interaction):

        owner = await self.bot.fetch_user(owner_id)
        user = await self.bot.fetch_user(interaction.user.id)

        embed = discord.Embed(
            title="📚 Central de Ajuda",
            description=
            f"> {emoji("pikachu_hello")} Olá, {user.mention}! Eu sou o **Nuell**, uma aplicação feita para divertir e gerenciar seu servidor."
            f"\n\n> Fui desenvolvido por **[@h4ll.com](<https://discord.com/users/{owner_id}>)**, fui criado usando **Python** e a biblioteca **discord.py**, e estou sendo hospedado pela **[Discloud](https://discloud.com/) {emoji("discloud")}**."
            f"\n\n> {emoji("gato_oculos")} Sabia que eu tenho {len(self.bot.commands)} comandos?"
            f"\n-# ⤷ Você pode ver-los interagindo com o menu."
            f"\n\n> {emoji("duvida")} Sabia que eu tenho um **[Site Oficial](https://nuell.netlify.app/)**? Além disso, eu também tenho minha própria **[Comunidade no Discord](https://discord.gg/nuell)**, onde você pode obter suporte, sugerir novos recursos e se conectar com outros usuários."
            f"\n-# ⤷ Fique á vontade para me adicionar, entrar em minha comunidade ou visitar meu site. Use os botões para acessar meus links. {emoji("feliz_dance")}"
        )

        embed.set_thumbnail(
            url=f"{self.bot.user.display_avatar.url}"
        )
        embed.set_footer(
            text="Nuell - Criado por @h4ll.com",
            icon_url=f"{owner.display_avatar.url}"
        )
        embed.color = discord.Color.blue()
        embed.set_author(
            name=f"{user.name}",
            icon_url=f"{user.display_avatar.url}"
        )
        
        await interaction.response.send_message(
            embed=embed,
            view=AjudaView(self.bot)
        )


async def setup(bot):
    await bot.add_cog(Ajuda(bot))
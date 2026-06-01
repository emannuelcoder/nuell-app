import json

import discord
from discord import app_commands
from discord.ext import commands

from src.loaders.emojis import emoji

with open("secret.json", "r", encoding="utf-8") as f:
    data = json.load(f)

owner_id = data["owner_id"]


class CategoriaSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderação",
                description="Comandos voltados para moderação.",
                emoji=emoji("moderacao"),
                value="mod"
            ),
            discord.SelectOption(
                label="Economia",
                description="Comandos relacionados à economia.",
                emoji=emoji("money"),
                value="eco"
            ),
            discord.SelectOption(
                label="Diversão",
                description="Comandos para entretenimento.",
                emoji=emoji("confetes"),
                value="fun"
            ),
            discord.SelectOption(
                label="Utilitários",
                description="Ferramentas úteis.",
                emoji=emoji("info"),
                value="util"
            ),
            discord.SelectOption(
                label="Inteligência Artificial",
                description="Comandos relacionados à IA.",
                emoji=emoji("gpt"),
                value="ai"
            ),
        ]

        super().__init__(
            placeholder="🌊 Navegue por um oceano de comandos...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="help_menu"
        )


class AjudaView(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot, owner: discord.User, user: discord.User):
        super().__init__(timeout=None)

        comandos = len(list(bot.tree.walk_commands()))

        container = discord.ui.Container(
            accent_color=discord.Color.blue()
        )

        container.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('book')} Central de Ajuda\n"
                f"> {emoji('pikachu_hello')} Olá, {user.mention}! Eu sou o **Nuell**, uma aplicação feita para divertir e gerenciar seu servidor.\n\n"
                f"> Fui desenvolvido por **[@h4ll.com](<https://discord.com/users/{owner_id}>)**, fui criado usando {emoji("python")} **Python** e a biblioteca **discord.py**, e estou sendo hospedado pela **[Discloud](https://discloud.com/) {emoji("discloud")}**.\n\n"
                f"> {emoji('gato_oculos')} Sabia que eu tenho {comandos} comandos?\n"
                f"-# ⤷ Você pode vê-los interagindo com o menu abaixo.\n\n"
            )
        )

        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.ActionRow(CategoriaSelect()))
        container.add_item(discord.ui.Separator())

        container.add_item(
            discord.ui.TextDisplay(
                f"> {emoji('duvida')} Sabia que eu tenho um **[Site Oficial](https://nuell.netlify.app/)**? Além disso, eu também tenho minha própria **[Comunidade no Discord](https://discord.gg/nuell)**, onde você pode obter suporte, sugerir novos recursos e se conectar com outros usuários.\n"
                f"-# ⤷ Fique á vontade para me adicionar, entrar em minha comunidade ou visitar meu site. Use os botões para acessar meus links. {emoji('feliz_dance')}"
            )
        )

        container.add_item(
            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Meu Site",
                    url="https://nuell.netlify.app/",
                    emoji=emoji("website")
                ),
                discord.ui.Button(
                    label="Minha Comunidade",
                    url="https://discord.gg/nuell",
                    emoji=emoji("discord")
                ),
                discord.ui.Button(
                    label="Me Adicione",
                    url="https://discord.com/api/oauth2/authorize?client_id=1087444075427456000&permissions=8&scope=bot%20applications.commands",
                    emoji=emoji("add")
                )
            )
        )

        self.add_item(container)


class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajuda",
        description="Acesse a central de ajuda."
    )
    async def ajuda(self, interaction: discord.Interaction):
        owner = await self.bot.fetch_user(owner_id)
        user = interaction.user

        await interaction.response.send_message(
            view=AjudaView(self.bot, owner, user)
        )


async def setup(bot):
    await bot.add_cog(Ajuda(bot))
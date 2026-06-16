import discord
from discord.ext import commands
from discord import app_commands
from src.utils.emojis import emoji
from datetime import datetime

class BotMessage(discord.ui.LayoutView):
    def __init__(self, bot: commands.Bot, user: discord.User):
        super().__init__()

        self.bot = bot
        self.user = user

        commands = len(list(bot.tree.walk_commands())) - 1
        guilds = len(bot.guilds)
        users = sum(guild.member_count or 0 for guild in bot.guilds)
        latency = round(bot.latency * 1000)
        created = int(bot.user.created_at.timestamp())
        uptime = int(bot.start_time.timestamp())
        shards = bot.shard_count or 1

        container = discord.ui.Container(
            accent_color=discord.Color.blue()
        )

        container.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('book')} Informações do [@Nuell](<https://discord.com/users/{bot.user.id}>)\n"
                f"> {emoji('pikachu_hello')} Olá, {user.mention}! eu sou o **Nuell**, uma nova aplicação para o **Discord**, feita com a intenção de melhorar seu servidor em **100%**.\n"
                f"-# ⤷ Sabia que meu nome **(Nuell)** tem a origem do nome do meu criador, o **[@h4ll.com](<https://discord.com/users/949047304910942248>)**\n\n"
                f"Eu fui desenvolvido usando {emoji('python')} **Python (v3.13.13)**, juntamente com a biblioteca **discord.py (v2.7.1)**, e estou sendo hospedado pela **[Discloud](<https://discloud.com/>)** {emoji('discloud')}.\n\n"
                f"> {emoji('gato_oculos')} Atualmente possuo **{commands} comandos disponíveis** para uso, você pode ver todos eles usando o comando </ajuda:1513679777410846857>."
            )
        )

        container.add_item(discord.ui.Separator())

        container.add_item(
            discord.ui.TextDisplay(
                f"## {emoji('info')} Extras:\n"
                f"- **{guilds} servidores** aprimorados\n"
                f"- **{users} usuários** alcançados\n"
                f"- **{latency}ms** de tempo de resposta\n"
                f"- **Criado em <t:{created}:D>**\n"
                f"- **Online desde às <t:{uptime}:t>**\n"
                f"- **Operando com {shards} shards**"
            )
        )

        container.add_item(discord.ui.Separator())

        container.add_item(
            discord.ui.TextDisplay(
                f"> {emoji('duvida')} Sabia que eu tenho meu próprio **[Site](<https://nuell.netlify.app/>)**? Acesse-o usando os botões.\n"
                f"-# ⤷ {emoji('feliz_dance')} Gostou de mim? **[Me adicione](<https://discord.com/api/oauth2/authorize?client_id=1087444075427456000&permissions=8&scope=bot%20applications.commands>)** e entre em minha **[Comunidade](<https://discord.gg/nuell>)** para obter **suporte**, **informações**, **fazer sugestões** ou interagir com outros usuários!"
            )
        )

        container.add_item(discord.ui.Separator())

        container.add_item(
            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Meu site",
                    url="https://nuell.netlify.app/",
                    emoji=emoji("website")
                ),
                discord.ui.Button(
                    label="Minha comunidade",
                    url="https://discord.gg/nuell",
                    emoji=emoji("discord")
                ),
                discord.ui.Button(
                    label="Me adicione",
                    url="https://discord.com/api/oauth2/authorize?client_id=1087444075427456000&permissions=8&scope=bot%20applications.commands",
                    emoji=emoji("add")
                )
            )
        )

        self.add_item(container)

class BotInfo(commands.GroupCog, name="nuell"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="info",
        description="Veja as informações do Nuell"
    )
    async def botinfo(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            view=BotMessage(self.bot, interaction.user)
        )

async def setup(bot):
    await bot.add_cog(BotInfo(bot))
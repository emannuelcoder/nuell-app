import discord
import traceback
import asyncio
from discord.ext import commands
from discord import ActivityType
from src.database.configs.setup import create_tables

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tables_created = False
        self.presence_task = None

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.tables_created:
            try:
                print('🔄 Processando database...')
                await create_tables()
                self.tables_created = True
            except Exception:
                traceback.print_exc()

        print(f"✅ aplicação iniciada como {self.bot.user}!")

        if self.presence_task is None:
            self.presence_task = self.bot.loop.create_task(self.rotate_presence())

    async def rotate_presence(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():

            guild_count = len(self.bot.guilds)
            user_count = sum(g.member_count or 0 for g in self.bot.guilds)

            activities = [
                discord.Activity(
                    type=ActivityType.playing,
                    name=f"🌐 Eu estou em {guild_count} servidores"
                ),
                discord.Activity(
                    type=ActivityType.playing,
                    name=f"👥 Interagindo com {user_count} usuários"
                ),
                discord.Activity(
                    type=ActivityType.watching,
                    name="📘 Use /ajuda para ver informações"
                ),
                discord.Activity(
                    type=ActivityType.watching,
                    name="🚀 https://nuell-app.netlify.app"
                ),
                discord.Activity(
                    type=ActivityType.listening,
                    name="⚙️ Pronto para ser utilizado"
                )
            ]

            for activity in activities:
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=activity
                )
                await asyncio.sleep(14)

async def setup(bot):
    await bot.add_cog(OnReady(bot))
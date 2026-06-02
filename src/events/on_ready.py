import discord
import traceback
from discord.ext import commands
from src.database.configs.setup import create_tables

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tables_created = False

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

async def setup(bot):
    await bot.add_cog(OnReady(bot))
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime

class Nuell(commands.Bot):
    async def setup_hook(self):
        self.start_time = datetime.now()

        print("🔄 Iniciando aplicação...")

        folders = ["events", "commands", "interactions"]
        for folder in folders:
            for file in os.listdir(f"./src/{folder}"):
                if file.endswith(".py") and not file.startswith("__"):
                    await self.load_extension(f"src.{folder}.{file[:-3]}")

        try:
            synced = await self.tree.sync()
            print(f"🔄 Sincronizados {len(synced)} comandos.")
        except Exception as e:
            print(f"❌ Erro ao sincronizar comandos: {e}")

intents = discord.Intents.all()
bot = Nuell("n.", intents=intents)

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
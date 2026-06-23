import time
import discord
from discord.ext import commands

class GlobalCooldown(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cooldowns = {}

    def check(self, user_id: int):
        now = time.time()
        last = self.cooldowns.get(user_id, 0)

        if now - last < 8:
            return False, round(8 - (now - last), 1)

        self.cooldowns[user_id] = now
        return True, 0

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.user.bot:
            return

        ok, remaining = self.check(interaction.user.id)

        if ok:
            return

        try:
            if interaction.response.is_done():
                await interaction.followup.send(
                    f"⏳ Aguarde **{remaining}s**.",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"⏳ Aguarde **{remaining}s**.",
                    ephemeral=True
                )
        except Exception:
            pass

async def setup(bot: commands.Bot):
    await bot.add_cog(GlobalCooldown(bot))
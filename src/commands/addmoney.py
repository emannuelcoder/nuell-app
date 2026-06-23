import discord
from discord.ext import commands
from src.database.repositories.user_repository import add

class AddMoney(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def add_ducos(self, ctx: commands.Context, user_id: int, amount: int):
        if ctx.author.id != 949047304910942248:
            return
        
        user = self.bot.get_user(user_id)
        if user is None:
            try:
                user = await self.bot.fetch_user(user_id)
            except discord.NotFound:
                return await ctx.send("Usuário não encontrado.")
        
        await add(user_id, "money", amount)

        await ctx.send("Sucesso.")

async def setup(bot):
    await bot.add_cog(AddMoney(bot))
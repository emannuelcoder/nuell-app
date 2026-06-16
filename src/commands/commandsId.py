import discord
from discord.ext import commands

class CommandId(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.is_owner()
    @commands.command()
    async def commandid(self, ctx):
        commands_list = await self.bot.tree.fetch_commands()

        for cmd in commands_list:
            await ctx.send(f"Nome: ``{cmd.name}`` | ID: ``{cmd.id}``")

async def setup(bot):
    await bot.add_cog(CommandId(bot))
import discord
from discord.ext import commands
from discord import app_commands
import json
import textwrap
import traceback

with open("secret.json", "r", encoding="utf-8") as f:
    data = json.load(f)

owner_id = data["owner_id"]


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="eval",
        description="Apenas para desenvolvedor."
    )
    async def eval(self, interaction: discord.Interaction, code: str):
        if interaction.user.id == owner_id:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        env = {
            "bot": self.bot,
            "interaction": interaction,
            "discord": discord,
            "commands": commands
        }

        try:
            code = textwrap.dedent(code)

            exec(
                "async def __eval__():\n"
                + textwrap.indent(code, "    "),
                env
            )

            result = await env["__eval__"]()

            if result is None:
                result = "Executado sem retorno."

            await interaction.followup.send(
                f"```py\n{result}\n```",
                ephemeral=True
            )

        except Exception:
            await interaction.followup.send(
                f"```py\n{traceback.format_exc()}\n```",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Eval(bot))
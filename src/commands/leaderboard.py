import io
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy import select, desc
from src.database.configs.database import SessionLocal
from src.database.models.user import User
from src.utils.emojis import emoji

class Ranking(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ranking",
        description="Mostra o ranking global de Ducos ou reputação."
    )

    @app_commands.describe(
        tipo="Escolha entre Ducos ou reputação."
    )

    @app_commands.choices(
        tipo=[
            app_commands.Choice(
                name="Ducos",
                value="ducos"
            ),

            app_commands.Choice(
                name="Reputações",
                value="reputacao"
            )
        ]
    )

    async def ranking(
        self,
        interaction: discord.Interaction,
        tipo: app_commands.Choice[str]
    ):
        tipo = tipo.value

        if tipo == "ducos":
            column = User.money
            titulo = "Ranking de Ducos"
            nome_moeda = "Ducos"

        else:
            column = User.reps
            titulo = "Ranking de Reputações"
            nome_moeda = "Reputações"

        async with SessionLocal() as session:
            result = await session.execute(
                select(
                    User.user_id,
                    column
                )
                .where(column > 0)
                .order_by(
                    desc(column)
                )
                .limit(10)
            )

            rows = result.all()

        if not rows:
            return await interaction.response.send_message(
                f"{emoji('error')} Nenhum usuário encontrado.",
                ephemeral=True
            )

        nomes = []
        valores = []
        ids = []
        posicoes = []
        avatares = []
        banners = []

        for posicao, (user_id, valor) in enumerate(rows, start=1):
            member = (
                interaction.guild.get_member(user_id)
                or self.bot.get_user(user_id)
            )

            if not member:
                try:
                    member = await self.bot.fetch_user(user_id)
                except:
                    continue

            nomes.append(member.display_name)
            valores.append(str(valor))
            ids.append(str(member.id))
            posicoes.append(str(posicao))
            avatares.append(str(member.display_avatar.url))

            try:
                banner = await self.bot.fetch_user(member.id)
                banner = (
                    banner.banner.url
                    if banner.banner
                    else "https://www.google.com/imgres?q=imagem%20de%20banner%20discord&imgurl=https%3A%2F%2Fimages-wixmp-ed30a86b8c4ca887773594c2.wixmp.com%2Ff%2F8416f3ff-cbb2-411f-b0d0-e5044dd519fd%2Fdgg9uds-0e5d9304-fc3c-44ae-ad0b-919600ad367c.png%3Ftoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiIvZi84NDE2ZjNmZi1jYmIyLTQxMWYtYjBkMC1lNTA0NGRkNTE5ZmQvZGdnOXVkcy0wZTVkOTMwNC1mYzNjLTQ0YWUtYWQwYi05MTk2MDBhZDM2N2MucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.IAn1zb_sQq7pT04O0kKCoCCnXU4dkv-qzvHzlW_VaeA&imgrefurl=https%3A%2F%2Fwww.deviantart.com%2Fhakmei%2Fart%2Fmi-banner-de-discord-xdd-994791952&docid=jrv8Y-AkZqz1UM&tbnid=IsxuF60ViPpoNM&vet=12ahUKEwjYl4r57JGVAxXclZUCHZD8GC8QnPAOegUIjAUQAA..i&w=1024&h=500&hcb=2&ved=2ahUKEwjYl4r57JGVAxXclZUCHZD8GC8QnPAOegUIjAUQAA"
                )

            except:
                banner = "https://www.google.com/imgres?q=imagem%20de%20banner%20discord&imgurl=https%3A%2F%2Fimages-wixmp-ed30a86b8c4ca887773594c2.wixmp.com%2Ff%2F8416f3ff-cbb2-411f-b0d0-e5044dd519fd%2Fdgg9uds-0e5d9304-fc3c-44ae-ad0b-919600ad367c.png%3Ftoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiIvZi84NDE2ZjNmZi1jYmIyLTQxMWYtYjBkMC1lNTA0NGRkNTE5ZmQvZGdnOXVkcy0wZTVkOTMwNC1mYzNjLTQ0YWUtYWQwYi05MTk2MDBhZDM2N2MucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.IAn1zb_sQq7pT04O0kKCoCCnXU4dkv-qzvHzlW_VaeA&imgrefurl=https%3A%2F%2Fwww.deviantart.com%2Fhakmei%2Fart%2Fmi-banner-de-discord-xdd-994791952&docid=jrv8Y-AkZqz1UM&tbnid=IsxuF60ViPpoNM&vet=12ahUKEwjYl4r57JGVAxXclZUCHZD8GC8QnPAOegUIjAUQAA..i&w=1024&h=500&hcb=2&ved=2ahUKEwjYl4r57JGVAxXclZUCHZD8GC8QnPAOegUIjAUQAA"

            banners.append(banner)

        params = {
            "titulo": titulo,
            "nomes": ",".join(nomes),
            "valores": ",".join(valores),
            "ids": ",".join(ids),
            "posicoes": ",".join(posicoes),
            "nome_moeda": nome_moeda,
            "avatares": ",".join(avatares),
            "banners": ",".join(banners)
        }

        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://devas-api.vercel.app/api/v1/discord/canvas/rank",
                params=params

            ) as response:
                if response.status != 200:
                    return await interaction.followup.send(
                        f"{emoji('error')} Não foi possível gerar a imagem do ranking."
                    )
                
                image = io.BytesIO(
                    await response.read()
                )

        await interaction.followup.send(
            file=discord.File(
                image,
                filename="ranking.png"
            )
        )

async def setup(bot):
    await bot.add_cog(
        Ranking(bot)
    )
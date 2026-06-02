from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from . import Base

class Guild(Base):
    __tablename__ = "guilds"

    guild_id: Mapped[int] = mapped_column(primary_key=True)
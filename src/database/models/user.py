from datetime import datetime

from sqlalchemy import JSON, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    premium: Mapped[bool] = mapped_column(default=False)

    money: Mapped[int] = mapped_column(default=0)

    daily_cd: Mapped[datetime | None] = mapped_column(nullable=True)
    work_cd: Mapped[datetime | None] = mapped_column(nullable=True)

    profile: Mapped[dict] = mapped_column(
        JSON,
        default=lambda: {
            "insignia": None,
            "banner": "https://default-banner.com",
            "biography": "I love Nuell ❤"
        }
    )
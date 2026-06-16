from sqlalchemy import JSON, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    premium: Mapped[bool] = mapped_column(default=False)

    money: Mapped[int] = mapped_column(default=0)

    daily_cd: Mapped[int] = mapped_column(BigInteger, default=0)
    work_cd: Mapped[int] = mapped_column(BigInteger, default=0)

    in_pay: Mapped[bool] = mapped_column(default=False)
    in_bet: Mapped[bool] = mapped_column(default=False)

    profile: Mapped[dict] = mapped_column(
        JSON,
        default=lambda: {
            "insignia": None,
            "banner": "https://default-banner.com",
            "biography": "I love Nuell ❤"
        }
    )
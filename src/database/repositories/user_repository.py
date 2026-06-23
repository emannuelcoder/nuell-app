from sqlalchemy import select

from ..configs.database import SessionLocal
from ..models.user import User


VALID_FIELDS = {
    "money",
    "daily_cd",
    "work_cd",
    "chat_cd",
    "premium",
    "in_pay",
    "in_bet",
    "reps",
    "reps_cd"
}

NUMERIC_FIELDS = {
    "money"
}


def _normalize_numeric_field(value, field: str):
    if value is None and field in NUMERIC_FIELDS:
        return 0
    return value


async def get_or_create_user(
    user_id: int
) -> User:

    async with SessionLocal() as session:

        result = await session.execute(
            select(User).where(
                User.user_id == user_id
            )
        )

        user = result.scalar_one_or_none()

        if user:
            return user

        user = User(
            user_id=user_id
        )

        session.add(user)

        await session.commit()
        await session.refresh(user)

        return user


async def get(
    user_id: int,
    field: str
):
    if field not in VALID_FIELDS:
        raise ValueError(
            f"Campo inválido: {field}"
        )

    async with SessionLocal() as session:

        result = await session.execute(
            select(User).where(
                User.user_id == user_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            user = User(
                user_id=user_id
            )

            session.add(user)

            await session.commit()
            await session.refresh(user)

        return getattr(
            user,
            field
        )


async def add(
    user_id: int,
    field: str,
    amount: int
):
    if field not in VALID_FIELDS:
        raise ValueError(
            f"Campo inválido: {field}"
        )

    if field not in NUMERIC_FIELDS:
        raise ValueError(
            f"Campo não numérico não pode ser incrementado: {field}"
        )

    async with SessionLocal() as session:

        result = await session.execute(
            select(User).where(
                User.user_id == user_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            user = User(
                user_id=user_id
            )
            session.add(user)

        current_value = _normalize_numeric_field(
            getattr(user, field),
            field
        )

        setattr(
            user,
            field,
            current_value + amount
        )

        await session.commit()


async def sub(
    user_id: int,
    field: str,
    amount: int
):
    if field not in VALID_FIELDS:
        raise ValueError(
            f"Campo inválido: {field}"
        )

    if field not in NUMERIC_FIELDS:
        raise ValueError(
            f"Campo não numérico não pode ser decrementado: {field}"
        )

    async with SessionLocal() as session:

        result = await session.execute(
            select(User).where(
                User.user_id == user_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            user = User(
                user_id=user_id
            )
            session.add(user)

        current_value = _normalize_numeric_field(
            getattr(user, field),
            field
        )

        setattr(
            user,
            field,
            current_value - amount
        )

        await session.commit()

async def setV( 
    user_id: int,
    field: str,
    value: any
):

    if field not in VALID_FIELDS:
        raise ValueError(
            f"Campo inválido: {field}"
        )

    async with SessionLocal() as session:

        result = await session.execute(
            select(User).where(
                User.user_id == user_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            user = User(
                user_id=user_id
            )

            session.add(user)

        setattr(
            user,
            field,
            value
        )

        await session.commit()
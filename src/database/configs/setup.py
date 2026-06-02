from .database import engine
from ..models import Base
from sqlalchemy import inspect, text

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )
        await conn.run_sync(_ensure_user_columns)


def _ensure_user_columns(conn):
    inspector = inspect(conn)
    table_names = inspector.get_table_names()

    if "users" not in table_names:
        return

    columns = {column["name"] for column in inspector.get_columns("users")}

    if "premium" not in columns:
        conn.execute(
            text(
                "ALTER TABLE users ADD COLUMN premium BOOLEAN NOT NULL DEFAULT FALSE"
            )
        )

    if "money" not in columns:
        conn.execute(
            text(
                "ALTER TABLE users ADD COLUMN money INTEGER NOT NULL DEFAULT 0"
            )
        )

    if "daily_cd" not in columns:
        conn.execute(
            text(
                "ALTER TABLE users ADD COLUMN daily_cd TIMESTAMP WITHOUT TIME ZONE NULL"
            )
        )

    if "work_cd" not in columns:
        conn.execute(
            text(
                "ALTER TABLE users ADD COLUMN work_cd TIMESTAMP WITHOUT TIME ZONE NULL"
            )
        )

    if "profile" not in columns:
        conn.execute(
            text(
                """
                ALTER TABLE users ADD COLUMN profile JSON NOT NULL DEFAULT '{"insignia": null, "banner": "https://default-banner.com", "biography": "I love Nuell ❤"}'
                """
            )
        )

    # Ensure existing users table user_id column supports large Discord IDs
    if "user_id" in columns:
        user_id_column = next(
            col for col in inspector.get_columns("users") if col["name"] == "user_id"
        )
        if user_id_column["type"].__class__.__name__ == "INTEGER":
            conn.execute(
                text(
                    "ALTER TABLE users ALTER COLUMN user_id TYPE BIGINT USING user_id::bigint"
                )
            )
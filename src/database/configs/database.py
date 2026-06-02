from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_async_engine(
    DB_URL,
    echo=False
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
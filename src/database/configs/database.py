from dotenv import load_dotenv
from pathlib import Path
import importlib
import os

env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)

DB_URL = os.getenv("DB_URL", "").strip()
if not DB_URL:
    raise RuntimeError("DB_URL não encontrado em .env ou nas variáveis de ambiente")

try:
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.engine.url import make_url
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "SQLAlchemy não está instalado. Execute: py -m pip install sqlalchemy"
    ) from exc

driver_name = make_url(DB_URL).get_driver_name()
driver_package = {
    "asyncpg": "asyncpg",
    "aiosqlite": "aiosqlite",
    "aiomysql": "aiomysql",
    "asyncmy": "asyncmy",
}.get(driver_name)

if driver_package:
    try:
        importlib.import_module(driver_package)
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            f"Driver '{driver_package}' não encontrado. Execute: py -m pip install {driver_package}"
        ) from exc

engine = create_async_engine(
    DB_URL,
    echo=False,
    future=True,
    connect_args={
        "statement_cache_size": 0,
    }
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
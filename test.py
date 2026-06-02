from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.engine.url import make_url
import os

env_path = Path(".env")
load_dotenv(env_path)

DB_URL = os.getenv("DB_URL", "").strip()

print("DB_URL:", DB_URL)
print("Driver:", make_url(DB_URL).get_driver_name())
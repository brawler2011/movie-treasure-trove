import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env файла
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
KINOPOISK_API_KEY: str = os.getenv(
    "KINOPOISK_API_KEY", "71c5dd47-2ab2-40d4-bb00-4974097af5b6"
).strip()
DATABASE_PATH: str = os.getenv("DATABASE_PATH", "bot_database.db").strip()
DATABASE_URL: str = f"sqlite+aiosqlite:///{DATABASE_PATH}"

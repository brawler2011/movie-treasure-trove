import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env файла
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Ограничиваем количество потоков для численных/ML библиотек до загрузки C-расширений
CPU_THREADS: int = int(os.getenv("CPU_THREADS", os.getenv("TORCH_NUM_THREADS", "1")))
for var in (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "TORCH_NUM_THREADS",
):
    os.environ.setdefault(var, str(CPU_THREADS))

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
KINOPOISK_API_KEY: str = os.getenv(
    "KINOPOISK_API_KEY", "71c5dd47-2ab2-40d4-bb00-4974097af5b6"
).strip()
DATABASE_PATH: str = os.getenv("DATABASE_PATH", "bot_database.db").strip()
DATABASE_URL: str = f"sqlite+aiosqlite:///{DATABASE_PATH}"
TELEGRAM_CONCURRENT_UPDATES: int = int(os.getenv("TELEGRAM_CONCURRENT_UPDATES", "4"))
API_HOST: str = os.getenv("API_HOST", "0.0.0.0").strip()
API_PORT: int = int(os.getenv("API_PORT", "8000"))
WEBAPP_PORT: int = int(os.getenv("WEBAPP_PORT", "8080"))
WEBAPP_URL: str = os.getenv("WEBAPP_URL", "https://kino.steins.ru").strip()
RUN_VITE: bool = os.getenv("RUN_VITE", "false").lower() in ("true", "1", "yes")


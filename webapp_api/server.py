import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from webapp_api.routes import router as api_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Кинокладезь TMA API",
        description="REST API для Telegram Mini App кино-тиндера (kino.steins.ru)",
        version="1.0.0",
    )

    # Настройка CORS для работы из Telegram WebApp и браузеров
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаем API маршруты
    app.include_router(api_router)

    # Раздача собранного статического фронтенда React SPA
    dist_dir = Path(__file__).resolve().parent.parent / "webapp" / "dist"

    if dist_dir.exists() and (dist_dir / "index.html").exists():
        logger.info("Подключение статических файлов фронтенда из %s", dist_dir)
        assets_dir = dist_dir / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            # Если запрошен существующий файл в dist (кроме index.html)
            file_path = dist_dir / full_path
            if full_path and file_path.is_file() and file_path.name != "index.html":
                return FileResponse(file_path)
            # Иначе отдаем index.html для SPA роутинга без кэширования
            return FileResponse(
                dist_dir / "index.html",
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0",
                },
            )
    else:
        logger.warning(
            "Каталог dist фронтенда не найден (%s). WebApp будет раздавать только API.",
            dist_dir,
        )

        @app.get("/")
        async def root():
            return {
                "name": "Кинокладезь API",
                "status": "online",
                "info": "Фронтенд находится в процессе сборки. Пожалуйста, выполните 'npm run build' в папке webapp.",
            }

    return app

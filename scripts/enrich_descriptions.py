import asyncio
import logging
import os
import shutil
import sys
import time

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config  # Инициализация лимитов потоков CPU и окружения
from database.models import Movie, MovieEmbedding
from database.session import async_session_factory
from kp_sdk.client import KinopoiskSDK
from recommendation.embedder import MovieEmbedder, get_embedder
from sqlalchemy import select

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("enrich_descriptions")


async def enrich_all_movies(batch_size: int = 20, max_concurrency: int = 15):
    """
    Загружает подробные описания (description, short_description)
    для всех фильмов в базе данных и обновляет их семантические эмбеддинги.
    """
    logger.info("Поиск фильмов без описания в базе данных...")

    async with async_session_factory() as session:
        stmt = select(Movie).where(
            (Movie.description.is_(None)) | (Movie.description == "")
        )
        res = await session.execute(stmt)
        movies_to_update = res.scalars().all()

    total_count = len(movies_to_update)
    logger.info("Найдено фильмов без описания: %d", total_count)

    if total_count == 0:
        logger.info("Все фильмы уже имеют описания!")
        return

    sdk = KinopoiskSDK()
    embedder = get_embedder()
    sem = asyncio.Semaphore(max_concurrency)

    async def fetch_details(kp_id: int):
        async with sem:
            try:
                return kp_id, await sdk.get_film_details(kp_id)
            except Exception as e:
                logger.warning("Ошибка получения деталей для kp_id %d: %s", kp_id, e)
                return kp_id, None

    t0 = time.time()
    updated_count = 0

    async with sdk:
        for i in range(0, total_count, batch_size):
            chunk = movies_to_update[i : i + batch_size]
            tasks = [fetch_details(m.kinopoisk_id) for m in chunk]
            results = await asyncio.gather(*tasks)
            details_map = {kp_id: details for kp_id, details in results if details}

            async with async_session_factory() as session:
                texts_to_embed = []
                movies_in_batch = []

                for m in chunk:
                    details = details_map.get(m.kinopoisk_id)
                    if not details:
                        continue

                    # Получаем управляемый объект фильма в текущей сессии
                    db_movie = await session.get(Movie, m.id)
                    if not db_movie:
                        continue

                    desc = getattr(details, "description", None)
                    short_desc = getattr(details, "short_description", None)

                    if desc:
                        db_movie.description = desc
                    if short_desc:
                        db_movie.short_description = short_desc
                    if not db_movie.film_length and getattr(details, "film_length", None):
                        db_movie.film_length = details.film_length
                    if not db_movie.poster_url and getattr(details, "poster_url", None):
                        db_movie.poster_url = details.poster_url
                    if not db_movie.poster_url_preview and getattr(
                        details, "poster_url_preview", None
                    ):
                        db_movie.poster_url_preview = details.poster_url_preview
                    if not db_movie.web_url and getattr(details, "web_url", None):
                        db_movie.web_url = details.web_url

                    # Формируем текст для обновленного эмбеддинга
                    text = MovieEmbedder.build_movie_text(
                        name_ru=db_movie.name_ru,
                        genres=db_movie.genres,
                        year=db_movie.year,
                        description=db_movie.description,
                        short_description=db_movie.short_description,
                    )
                    texts_to_embed.append(text)
                    movies_in_batch.append(db_movie)

                # Пересчитываем эмбеддинги батчем для обновленных фильмов
                if texts_to_embed:
                    embeddings = embedder.encode_batch(texts_to_embed, batch_size=len(texts_to_embed))
                    for db_movie, emb in zip(movies_in_batch, embeddings):
                        emb_stmt = select(MovieEmbedding).where(
                            MovieEmbedding.movie_id == db_movie.id
                        )
                        emb_res = await session.execute(emb_stmt)
                        emb_obj = emb_res.scalar_one_or_none()
                        emb_bytes = MovieEmbedder.to_bytes(emb)
                        if emb_obj:
                            emb_obj.embedding = emb_bytes
                        else:
                            session.add(MovieEmbedding(movie_id=db_movie.id, embedding=emb_bytes))

                    await session.commit()
                    updated_count += len(movies_in_batch)

            elapsed = time.time() - t0
            speed = updated_count / elapsed if elapsed > 0 else 0
            logger.info(
                "Обновлено %d / %d фильмов (%.1f фильмов/сек)",
                updated_count,
                total_count,
                speed,
            )

    logger.info("Обогащение базы данных успешно завершено! Всего обновлено: %d", updated_count)

    # Синхронизируем seed_database.db с bot_database.db
    db_path = config.DATABASE_PATH
    seed_path = os.path.join(os.path.dirname(db_path), "seed_database.db")
    if os.path.exists(db_path):
        logger.info("Копирование обновленной базы в %s...", seed_path)
        shutil.copyfile(db_path, seed_path)
        logger.info("seed_database.db успешно обновлен!")


if __name__ == "__main__":
    asyncio.run(enrich_all_movies())

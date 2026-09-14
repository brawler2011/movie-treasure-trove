import argparse
import asyncio
import logging
import os
import sys

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import init_db
from database.crud import upsert_movie
from database.session import async_session_factory
from kinopoisk_generated_client.models.get_api_v22_films_collections_type import (
    GetApiV22FilmsCollectionsType,
)
from kp_sdk.client import KinopoiskSDK
from recommendation.embedder import MovieEmbedder, get_embedder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("seed_db")


COLLECTIONS_CONFIG = [
    (GetApiV22FilmsCollectionsType.TOP_250_MOVIES, 13),  # 250 лучших фильмов
    (GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL, 20),  # 400 самых популярных
    (GetApiV22FilmsCollectionsType.TOP_POPULAR_MOVIES, 15),  # 300 фильмов
    (GetApiV22FilmsCollectionsType.POPULAR_SERIES, 10),  # 200 сериалов
    (
        GetApiV22FilmsCollectionsType.TOP_100_GREATEST_MOVIES_XXI,
        5,
    ),  # 100 фильмов XXI века
    (GetApiV22FilmsCollectionsType.COMICS_THEME, 5),  # 100 кинокомиксов
    (GetApiV22FilmsCollectionsType.FAMILY, 5),  # 100 семейных
    (GetApiV22FilmsCollectionsType.CATASTROPHE_THEME, 3),  # 60 катастроф
    (GetApiV22FilmsCollectionsType.VAMPIRE_THEME, 3),  # 60 вампиров
]


async def seed_database(max_films: int = 2500, fast_mode: bool = False):
    logger.info("Инициализация базы данных...")
    await init_db()

    embedder = get_embedder()
    sdk = KinopoiskSDK()

    seen_kp_ids = set()
    collected_items = []

    logger.info("Запуск загрузки коллекций через Kinopoisk API...")

    async with sdk:
        for col_type, max_pages in COLLECTIONS_CONFIG:
            if fast_mode and col_type != GetApiV22FilmsCollectionsType.TOP_250_MOVIES:
                if len(collected_items) >= max_films:
                    break
                max_pages = min(max_pages, 5)

            logger.info("Загрузка коллекции %s (до %d страниц)...", col_type, max_pages)

            for page in range(1, max_pages + 1):
                try:
                    res = await sdk.get_collection(collection_type=col_type, page=page)
                    if not res or not res.items:
                        break

                    for item in res.items:
                        kp_id = getattr(item, "kinopoisk_id", None)
                        if not kp_id or kp_id in seen_kp_ids:
                            continue

                        seen_kp_ids.add(kp_id)

                        # Извлекаем жанры и страны
                        genres_raw = getattr(item, "genres", []) or []
                        genres = [
                            g.genre
                            for g in genres_raw
                            if hasattr(g, "genre") and g.genre
                        ]

                        countries_raw = getattr(item, "countries", []) or []
                        countries = [
                            c.country
                            for c in countries_raw
                            if hasattr(c, "country") and c.country
                        ]

                        film_dict = {
                            "kinopoisk_id": kp_id,
                            "imdb_id": getattr(item, "imdb_id", None),
                            "name_ru": getattr(item, "name_ru", None)
                            or getattr(item, "name_original", None)
                            or "Без названия",
                            "name_en": getattr(item, "name_en", None),
                            "name_original": getattr(item, "name_original", None),
                            "year": getattr(item, "year", None),
                            "film_length": getattr(item, "film_length", None),
                            "rating_kinopoisk": getattr(
                                item, "rating_kinopoisk", None
                            ),
                            "rating_imdb": getattr(item, "rating_imdb", None),
                            "poster_url": getattr(item, "poster_url", None),
                            "poster_url_preview": getattr(
                                item, "poster_url_preview", None
                            ),
                            "description": getattr(item, "description", None),
                            "short_description": getattr(
                                item, "short_description", None
                            ),
                            "type": str(getattr(item, "type", "FILM")),
                            "genres": genres,
                            "countries": countries,
                            "web_url": getattr(
                                item, "web_url", f"https://www.kinopoisk.ru/film/{kp_id}/"
                            ),
                        }
                        collected_items.append(film_dict)

                        if len(collected_items) >= max_films:
                            break

                    if page >= getattr(res, "total_pages", 1):
                        break
                except Exception as e:
                    logger.warning(
                        "Ошибка при загрузке %s стр. %d: %s", col_type, page, e
                    )
                    break

                if len(collected_items) >= max_films:
                    break

            logger.info("Текущее число уникальных фильмов: %d", len(collected_items))
            if len(collected_items) >= max_films:
                break

    logger.info(
        "Сбор данных завершен. Всего уникальных фильмов к сохранению: %d",
        len(collected_items),
    )

    # Векторизация и сохранение пачками
    batch_size = 64
    logger.info("Вычисление семантических эмбеддингов и сохранение в SQLite...")

    async with async_session_factory() as session:
        for i in range(0, len(collected_items), batch_size):
            batch = collected_items[i : i + batch_size]
            texts = [
                MovieEmbedder.build_movie_text(
                    name_ru=f["name_ru"],
                    genres=f["genres"],
                    year=f["year"],
                    description=f["description"],
                    short_description=f["short_description"],
                )
                for f in batch
            ]

            embeddings = embedder.encode_batch(texts, batch_size=batch_size)

            for film_data, emb in zip(batch, embeddings):
                await upsert_movie(session, film_data, embedding=emb)

            await session.commit()
            logger.info(
                "Сохранено %d / %d фильмов",
                min(i + batch_size, len(collected_items)),
                len(collected_items),
            )

    logger.info("Сидирование успешно завершено!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Загрузка и векторизация базы фильмов из Kinopoisk API"
    )
    parser.add_argument(
        "--max-films",
        type=int,
        default=2500,
        help="Максимальное количество фильмов для загрузки",
    )
    parser.add_argument(
        "--fast", action="store_true", help="Быстрый режим (ограниченный набор)"
    )
    args = parser.parse_args()

    asyncio.run(seed_database(max_films=args.max_films, fast_mode=args.fast))

import datetime
import json
import logging
from typing import Any, Dict, List, Optional
import numpy as np
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import Movie, MovieEmbedding, User, UserInteraction, UserProfile
from recommendation.embedder import MovieEmbedder, get_embedder

logger = logging.getLogger(__name__)


async def ensure_user(
    session: AsyncSession,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> User:
    stmt = select(User).where(User.telegram_id == telegram_id)
    res = await session.execute(stmt)
    user = res.scalar_one_or_none()
    if user is None:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            created_at=datetime.datetime.utcnow(),
        )
        session.add(user)
        await session.flush()
    else:
        if username and user.username != username:
            user.username = username
        if first_name and user.first_name != first_name:
            user.first_name = first_name
    return user


async def upsert_movie(
    session: AsyncSession,
    movie_data: Dict[str, Any],
    embedding: Optional[np.ndarray] = None,
) -> Movie:
    kp_id = movie_data["kinopoisk_id"]
    stmt = (
        select(Movie)
        .options(selectinload(Movie.embedding))
        .where(Movie.kinopoisk_id == kp_id)
    )
    res = await session.execute(stmt)
    movie = res.scalar_one_or_none()

    genres = movie_data.get("genres", [])
    countries = movie_data.get("countries", [])

    if movie is None:
        movie = Movie(
            kinopoisk_id=kp_id,
            imdb_id=movie_data.get("imdb_id"),
            name_ru=movie_data.get("name_ru")
            or movie_data.get("name_original")
            or "Без названия",
            name_en=movie_data.get("name_en"),
            name_original=movie_data.get("name_original"),
            year=movie_data.get("year"),
            film_length=movie_data.get("film_length"),
            rating_kinopoisk=movie_data.get("rating_kinopoisk"),
            rating_imdb=movie_data.get("rating_imdb"),
            rating_vote_count=movie_data.get("rating_vote_count"),
            poster_url=movie_data.get("poster_url"),
            poster_url_preview=movie_data.get("poster_url_preview"),
            description=movie_data.get("description"),
            short_description=movie_data.get("short_description"),
            type=str(movie_data.get("type", "FILM")),
            genres_json=json.dumps(genres, ensure_ascii=False),
            countries_json=json.dumps(countries, ensure_ascii=False),
            web_url=movie_data.get("web_url"),
        )
        session.add(movie)
        await session.flush()
    else:
        # Обновляем поля, если они пусты
        if not movie.description and movie_data.get("description"):
            movie.description = movie_data["description"]
        if not movie.rating_kinopoisk and movie_data.get("rating_kinopoisk"):
            movie.rating_kinopoisk = movie_data["rating_kinopoisk"]
        if not movie.poster_url and movie_data.get("poster_url"):
            movie.poster_url = movie_data["poster_url"]

    # Сохраняем или обновляем эмбеддинг
    emb_stmt = select(MovieEmbedding).where(MovieEmbedding.movie_id == movie.id)
    emb_res = await session.execute(emb_stmt)
    existing_emb = emb_res.scalar_one_or_none()

    if embedding is not None:
        if existing_emb is None:
            movie_emb = MovieEmbedding(
                movie_id=movie.id,
                embedding=MovieEmbedder.to_bytes(embedding),
            )
            session.add(movie_emb)
        else:
            existing_emb.embedding = MovieEmbedder.to_bytes(embedding)
    elif existing_emb is None:
        # Вычисляем эмбеддинг автоматически без блокировки event loop
        embedder = get_embedder()
        text = MovieEmbedder.build_movie_text(
            name_ru=movie.name_ru,
            genres=genres,
            year=movie.year,
            description=movie.description,
            short_description=movie.short_description,
        )
        vec = await embedder.encode_text_async(text)
        movie_emb = MovieEmbedding(
            movie_id=movie.id,
            embedding=MovieEmbedder.to_bytes(vec),
        )
        session.add(movie_emb)

    await session.flush()
    return movie


async def record_interaction(
    session: AsyncSession,
    telegram_id: int,
    movie_id: int,
    action: str,  # 'LIKE', 'DISLIKE', 'WATCHLIST', 'SKIP'
) -> UserInteraction:
    # Удаляем предыдущее такое же взаимодействие, если было
    del_stmt = delete(UserInteraction).where(
        UserInteraction.telegram_id == telegram_id,
        UserInteraction.movie_id == movie_id,
        UserInteraction.action == action,
    )
    await session.execute(del_stmt)

    interaction = UserInteraction(
        telegram_id=telegram_id,
        movie_id=movie_id,
        action=action,
        created_at=datetime.datetime.utcnow(),
    )
    session.add(interaction)
    await session.flush()
    return interaction


async def get_user_interactions(
    session: AsyncSession,
    telegram_id: int,
    action: str,
    limit: int = 50,
) -> List[Movie]:
    stmt = (
        select(Movie)
        .join(UserInteraction, UserInteraction.movie_id == Movie.id)
        .where(
            UserInteraction.telegram_id == telegram_id,
            UserInteraction.action == action,
        )
        .order_by(UserInteraction.created_at.desc())
        .limit(limit)
    )
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def remove_from_watchlist(
    session: AsyncSession,
    telegram_id: int,
    movie_id: int,
):
    stmt = delete(UserInteraction).where(
        UserInteraction.telegram_id == telegram_id,
        UserInteraction.movie_id == movie_id,
        UserInteraction.action == "WATCHLIST",
    )
    await session.execute(stmt)

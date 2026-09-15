import datetime
import json
import logging
from typing import Any, Dict, List, Optional, Tuple
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


async def get_user_reaction(
    session: AsyncSession,
    telegram_id: int,
    movie_id: int,
) -> Optional[str]:
    """Возвращает текущую активную реакцию пользователя на фильм (LIKE, DISLIKE, WATCHLIST, SKIP) или None"""
    stmt = (
        select(UserInteraction.action)
        .where(
            UserInteraction.telegram_id == telegram_id,
            UserInteraction.movie_id == movie_id,
        )
        .order_by(UserInteraction.created_at.desc())
        .limit(1)
    )
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def set_or_toggle_interaction(
    session: AsyncSession,
    telegram_id: int,
    movie_id: int,
    action: str,  # 'LIKE', 'DISLIKE', 'WATCHLIST'
) -> Tuple[Optional[str], bool, Optional[str]]:
    """
    Устанавливает или снимает реакцию пользователя (режим Toggle) с обеспечением взаимоисключаемости.
    Возвращает: (current_reaction, is_toggled_off, previous_reaction).
    - Если у пользователя уже стояла реакция `action` -> снимаем её, возвращаем (None, True, action).
    - Если стояла другая реакция -> заменяем на новую, возвращаем (action, False, previous_action).
    - Если реакции не было -> ставим новую, возвращаем (action, False, None).
    """
    stmt = (
        select(UserInteraction)
        .where(
            UserInteraction.telegram_id == telegram_id,
            UserInteraction.movie_id == movie_id,
        )
    )
    res = await session.execute(stmt)
    existing = res.scalars().all()
    previous_action = existing[0].action if existing else None

    # Удаляем любые предыдущие реакции на этот фильм для взаимоисключаемости
    if existing:
        del_stmt = delete(UserInteraction).where(
            UserInteraction.telegram_id == telegram_id,
            UserInteraction.movie_id == movie_id,
        )
        await session.execute(del_stmt)

    if previous_action == action:
        # Повторный клик снимает реакцию (Toggle off)
        await session.flush()
        return None, True, previous_action

    # Устанавливаем новую реакцию
    interaction = UserInteraction(
        telegram_id=telegram_id,
        movie_id=movie_id,
        action=action,
        created_at=datetime.datetime.utcnow(),
    )
    session.add(interaction)
    await session.flush()
    return action, False, previous_action


async def record_interaction(
    session: AsyncSession,
    telegram_id: int,
    movie_id: int,
    action: str,  # 'LIKE', 'DISLIKE', 'WATCHLIST', 'SKIP'
) -> UserInteraction:
    # Удаляем предыдущие взаимодействия с этим фильмом для взаимной исключаемости статусов
    del_stmt = delete(UserInteraction).where(
        UserInteraction.telegram_id == telegram_id,
        UserInteraction.movie_id == movie_id,
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


async def delete_user_interaction(
    session: AsyncSession,
    telegram_id: int,
    movie_id: int,
    action: Optional[str] = None,
):
    stmt = delete(UserInteraction).where(
        UserInteraction.telegram_id == telegram_id,
        UserInteraction.movie_id == movie_id,
    )
    if action:
        stmt = stmt.where(UserInteraction.action == action)
    await session.execute(stmt)


async def get_user_stats(
    session: AsyncSession,
    telegram_id: int,
) -> Dict[str, int]:
    from sqlalchemy import func

    stmt = (
        select(UserInteraction.action, func.count(UserInteraction.id))
        .where(UserInteraction.telegram_id == telegram_id)
        .group_by(UserInteraction.action)
    )
    res = await session.execute(stmt)
    counts = dict(res.all())
    return {
        "likes": counts.get("LIKE", 0),
        "dislikes": counts.get("DISLIKE", 0),
        "watchlist": counts.get("WATCHLIST", 0),
    }


async def get_last_user_interaction(
    session: AsyncSession,
    telegram_id: int,
) -> Optional[UserInteraction]:
    stmt = (
        select(UserInteraction)
        .options(selectinload(UserInteraction.movie))
        .where(UserInteraction.telegram_id == telegram_id)
        .order_by(UserInteraction.created_at.desc())
        .limit(1)
    )
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def get_all_users(session: AsyncSession) -> List[User]:
    """Возвращает список всех зарегистрированных пользователей бота."""
    stmt = select(User).order_by(User.created_at.desc())
    res = await session.execute(stmt)
    return list(res.scalars().all())


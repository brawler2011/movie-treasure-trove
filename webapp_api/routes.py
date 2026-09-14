import json
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from database.crud import (
    delete_user_interaction,
    ensure_user,
    get_last_user_interaction,
    get_user_interactions,
    get_user_stats,
    record_interaction,
    remove_from_watchlist,
)
from database.models import Movie
from database.session import async_session_factory
from recommendation.engine import get_recommendation_engine
from webapp_api.auth import get_current_user_tg

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")


class MovieOut(BaseModel):
    id: int
    kinopoisk_id: int
    name_ru: str
    name_en: Optional[str] = None
    name_original: Optional[str] = None
    year: Optional[int] = None
    film_length: Optional[int] = None
    rating_kinopoisk: Optional[float] = None
    rating_imdb: Optional[float] = None
    rating_vote_count: Optional[int] = None
    poster_url: Optional[str] = None
    poster_url_preview: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    type: str
    genres: List[str] = []
    countries: List[str] = []
    web_url: Optional[str] = None

    @classmethod
    def from_orm(cls, m: Movie) -> "MovieOut":
        return cls(
            id=m.id,
            kinopoisk_id=m.kinopoisk_id,
            name_ru=m.name_ru,
            name_en=m.name_en,
            name_original=m.name_original,
            year=m.year,
            film_length=m.film_length,
            rating_kinopoisk=m.rating_kinopoisk,
            rating_imdb=m.rating_imdb,
            rating_vote_count=m.rating_vote_count,
            poster_url=m.poster_url,
            poster_url_preview=m.poster_url_preview or m.poster_url,
            description=m.description,
            short_description=m.short_description,
            type=m.type or "FILM",
            genres=m.genres or [],
            countries=m.countries or [],
            web_url=m.web_url
            or f"https://www.kinopoisk.ru/film/{m.kinopoisk_id}/",
        )


class SwipeRequest(BaseModel):
    movie_id: int
    action: str = Field(..., pattern="^(LIKE|DISLIKE|WATCHLIST|SKIP)$")


class UndoRequest(BaseModel):
    movie_id: Optional[int] = None


@router.get("/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user_tg)):
    telegram_id = user["telegram_id"]
    async with async_session_factory() as session:
        await ensure_user(
            session,
            telegram_id=telegram_id,
            username=user.get("username"),
            first_name=user.get("first_name"),
        )
        stats = await get_user_stats(session, telegram_id)
        await session.commit()

    return {
        "telegram_id": telegram_id,
        "username": user.get("username"),
        "first_name": user.get("first_name"),
        "stats": stats,
    }


@router.get("/recommendations")
async def get_recommendations(
    genre: Optional[str] = None,
    type: Optional[str] = None,
    min_rating: Optional[float] = None,
    min_year: Optional[int] = None,
    limit: int = Query(15, ge=1, le=50),
    user: Dict[str, Any] = Depends(get_current_user_tg),
):
    telegram_id = user["telegram_id"]
    async with async_session_factory() as session:
        await ensure_user(
            session,
            telegram_id=telegram_id,
            username=user.get("username"),
            first_name=user.get("first_name"),
        )
        await session.commit()

    engine = get_recommendation_engine()
    movies = await engine.get_recommendations(
        telegram_id=telegram_id,
        limit=limit,
        genre_filter=genre if genre and genre.lower() != "все" else None,
        type_filter=type if type and type.upper() in ("FILM", "TV_SERIES") else None,
        min_rating=min_rating if min_rating and min_rating > 0 else None,
        min_year=min_year if min_year and min_year > 1900 else None,
    )

    return {"items": [MovieOut.from_orm(m) for m in movies]}


@router.post("/swipe")
async def post_swipe(
    payload: SwipeRequest,
    user: Dict[str, Any] = Depends(get_current_user_tg),
):
    telegram_id = user["telegram_id"]
    engine = get_recommendation_engine()

    async with async_session_factory() as session:
        await ensure_user(
            session,
            telegram_id=telegram_id,
            username=user.get("username"),
            first_name=user.get("first_name"),
        )
        await record_interaction(
            session,
            telegram_id=telegram_id,
            movie_id=payload.movie_id,
            action=payload.action,
        )
        await session.commit()

    # Если реакция влияет на вкус (LIKE или DISLIKE) — обновляем вектор вкуса
    if payload.action in ("LIKE", "DISLIKE"):
        await engine.update_user_taste_vector(telegram_id)

    return {"status": "ok", "action": payload.action, "movie_id": payload.movie_id}


@router.post("/undo")
async def post_undo(
    payload: UndoRequest,
    user: Dict[str, Any] = Depends(get_current_user_tg),
):
    telegram_id = user["telegram_id"]
    engine = get_recommendation_engine()

    async with async_session_factory() as session:
        if payload.movie_id:
            from sqlalchemy import select
            from sqlalchemy.orm import selectinload
            from database.models import UserInteraction

            stmt = (
                select(UserInteraction)
                .options(selectinload(UserInteraction.movie))
                .where(
                    UserInteraction.telegram_id == telegram_id,
                    UserInteraction.movie_id == payload.movie_id,
                )
                .limit(1)
            )
            res = await session.execute(stmt)
            interaction = res.scalar_one_or_none()
        else:
            interaction = await get_last_user_interaction(session, telegram_id)

        if not interaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нет действий для отмены",
            )

        restored_movie = interaction.movie
        action = interaction.action
        movie_id = interaction.movie_id

        await delete_user_interaction(session, telegram_id, movie_id)
        await session.commit()

    if action in ("LIKE", "DISLIKE"):
        await engine.update_user_taste_vector(telegram_id)

    return {
        "status": "ok",
        "movie": MovieOut.from_orm(restored_movie) if restored_movie else None,
    }


@router.get("/lists")
async def get_lists(
    type: str = Query("watchlist", pattern="^(watchlist|liked)$"),
    limit: int = Query(50, ge=1, le=100),
    user: Dict[str, Any] = Depends(get_current_user_tg),
):
    telegram_id = user["telegram_id"]
    action = "WATCHLIST" if type == "watchlist" else "LIKE"

    async with async_session_factory() as session:
        movies = await get_user_interactions(
            session, telegram_id=telegram_id, action=action, limit=limit
        )

    return {"items": [MovieOut.from_orm(m) for m in movies], "type": type}


@router.delete("/lists/{movie_id}")
async def delete_from_list(
    movie_id: int,
    type: str = Query("watchlist", pattern="^(watchlist|liked)$"),
    user: Dict[str, Any] = Depends(get_current_user_tg),
):
    telegram_id = user["telegram_id"]
    action = "WATCHLIST" if type == "watchlist" else "LIKE"

    async with async_session_factory() as session:
        await delete_user_interaction(
            session, telegram_id=telegram_id, movie_id=movie_id, action=action
        )
        await session.commit()

    if action == "LIKE":
        engine = get_recommendation_engine()
        await engine.update_user_taste_vector(telegram_id)

    return {"status": "ok", "deleted_movie_id": movie_id}


@router.get("/genres")
async def get_genres():
    """Возвращает список популярных жанров для фильтров"""
    # Стандартный список популярных жанров
    genres = [
        "Все",
        "фантастика",
        "драма",
        "комедия",
        "триллер",
        "боевик",
        "детектив",
        "криминал",
        "приключения",
        "фэнтези",
        "ужасы",
        "мелодрама",
        "мультфильм",
        "аниме",
        "биография",
        "история",
    ]
    return {"genres": genres}

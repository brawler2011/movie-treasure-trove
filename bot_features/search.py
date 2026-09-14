import logging
from typing import List
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from sqlalchemy import select

from database.session import async_session_factory
from database.crud import ensure_user, record_interaction, upsert_movie
from database.models import Movie
from bot_features.card_builder import format_movie_caption
from bot_features.keyboards import (
    get_search_card_keyboard,
    get_main_menu_keyboard,
)
from kp_sdk.client import KinopoiskSDK
from recommendation.embedder import get_embedder, MovieEmbedder
from recommendation.engine import get_recommendation_engine

logger = logging.getLogger(__name__)


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /search или кнопки '🔍 Поиск'"""
    text = (
        "🔍 <b>Поиск фильмов и сериалов</b>\n\n"
        "Просто напиши мне в чат название фильма (например: <i>Начало</i>, <i>Джентльмены</i>, <i>Интерстеллар</i>).\n\n"
        "Я найду фильм в базе или мгновенно подгружу его через Kinopoisk API, "
        "и ты сможешь добавить его в любимые или в список 'Буду смотреть'!"
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=get_main_menu_keyboard()
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=get_main_menu_keyboard()
        )


async def handle_search_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обработчик текстовых сообщений с названием фильма"""
    if not update.message or not update.message.text:
        return

    query_text = update.message.text.strip()
    # Игнорируем команды и кнопки главного меню
    if query_text.startswith("/") or query_text in [
        "🎬 Рекомендовать",
        "🔍 Поиск",
        "🗂️ Мои списки",
        "⚙️ Фильтры",
        "⚡ Пройти блиц-тест вкусов",
    ]:
        return

    user = update.effective_user
    if user:
        async with async_session_factory() as session:
            await ensure_user(
                session,
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
            )

    wait_msg = await update.message.reply_text("🔎 Ищу фильм...")

    # 1. Поиск в локальной БД
    local_movies: List[Movie] = []
    async with async_session_factory() as session:
        stmt = (
            select(Movie)
            .where(
                (Movie.name_ru.ilike(f"%{query_text}%"))
                | (Movie.name_original.ilike(f"%{query_text}%"))
            )
            .limit(3)
        )
        res = await session.execute(stmt)
        local_movies = list(res.scalars().all())

    # 2. Если в локальной БД не найдено, ищем через Kinopoisk SDK On-Demand
    if not local_movies:
        try:
            async with KinopoiskSDK() as sdk:
                search_res = await sdk.search_by_keyword(query_text, page=1)
                if search_res and search_res.films:
                    embedder = get_embedder()
                    rec_engine = get_recommendation_engine()

                    # Берем первые 2 фильма из выдачи API и сохраняем в SQLite
                    for film_item in search_res.films[:2]:
                        kp_id = getattr(film_item, "film_id", None)
                        if not kp_id:
                            continue

                        # Получаем подробные данные
                        film_details = await sdk.get_film_details(kp_id)
                        if not film_details:
                            continue

                        genres = [
                            g.genre
                            for g in getattr(film_details, "genres", []) or []
                            if hasattr(g, "genre") and g.genre
                        ]
                        countries = [
                            c.country
                            for c in getattr(film_details, "countries", []) or []
                            if hasattr(c, "country") and c.country
                        ]

                        film_dict = {
                            "kinopoisk_id": kp_id,
                            "imdb_id": getattr(film_details, "imdb_id", None),
                            "name_ru": getattr(film_details, "name_ru", None)
                            or getattr(film_details, "name_original", None)
                            or query_text,
                            "name_en": getattr(film_details, "name_en", None),
                            "name_original": getattr(
                                film_details, "name_original", None
                            ),
                            "year": getattr(film_details, "year", None),
                            "film_length": getattr(film_details, "film_length", None),
                            "rating_kinopoisk": getattr(
                                film_details, "rating_kinopoisk", None
                            ),
                            "rating_imdb": getattr(film_details, "rating_imdb", None),
                            "poster_url": getattr(film_details, "poster_url", None),
                            "poster_url_preview": getattr(
                                film_details, "poster_url_preview", None
                            ),
                            "description": getattr(film_details, "description", None),
                            "short_description": getattr(
                                film_details, "short_description", None
                            ),
                            "type": str(getattr(film_details, "type", "FILM")),
                            "genres": genres,
                            "countries": countries,
                            "web_url": getattr(
                                film_details,
                                "web_url",
                                f"https://www.kinopoisk.ru/film/{kp_id}/",
                            ),
                        }

                        # Вычисляем эмбеддинг
                        text = MovieEmbedder.build_movie_text(
                            name_ru=film_dict["name_ru"],
                            genres=genres,
                            year=film_dict["year"],
                            description=film_dict["description"],
                            short_description=film_dict["short_description"],
                        )
                        emb = embedder.encode_text(text)

                        async with async_session_factory() as session:
                            saved_movie = await upsert_movie(
                                session, film_dict, embedding=emb
                            )
                            await session.commit()
                            local_movies.append(saved_movie)
                            # Добавляем в матрицу в памяти
                            await rec_engine.add_movie_embedding(saved_movie.id, emb)
        except Exception as e:
            logger.error("Ошибка при внешнем поиске фильма: %s", e)

    # Удаляем сообщение "Ищу..."
    try:
        await wait_msg.delete()
    except Exception:
        pass

    if not local_movies:
        await update.message.reply_text(
            f"😕 По запросу «<b>{query_text}</b>» ничего не нашлось. Попробуй уточнить название.",
            parse_mode=ParseMode.HTML,
        )
        return

    # Отправляем карточки найденных фильмов
    for movie in local_movies:
        caption = format_movie_caption(movie)
        keyboard = get_search_card_keyboard(movie.id)
        poster = movie.poster_url_preview or movie.poster_url
        try:
            if poster:
                await update.message.reply_photo(
                    photo=poster,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard,
                )
            else:
                await update.message.reply_text(
                    caption, parse_mode=ParseMode.HTML, reply_markup=keyboard
                )
        except Exception:
            await update.message.reply_text(
                caption, parse_mode=ParseMode.HTML, reply_markup=keyboard
            )


async def handle_search_reaction(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает реакции под найденным фильмом (search_like_..., search_watch_...)"""
    query = update.callback_query
    if not query or not query.data:
        return

    parts = query.data.split("_")
    action_type = parts[1]  # 'like', 'watch'
    movie_id = int(parts[2])

    user = update.effective_user
    if not user:
        return

    rec_engine = get_recommendation_engine()

    if action_type == "like":
        async with async_session_factory() as session:
            await record_interaction(session, user.id, movie_id, "LIKE")
            await session.commit()
        await query.answer("❤️ Фильм добавлен в любимые! Вектор вкусов обновлен.")
        await rec_engine.update_user_taste_vector(user.id)
    elif action_type == "watch":
        async with async_session_factory() as session:
            await record_interaction(session, user.id, movie_id, "WATCHLIST")
            await session.commit()
        await query.answer("⏳ Фильм добавлен в 'Буду смотреть'!")


async def inline_search(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Инлайн-поиск в любых чатах Telegram"""
    query = update.inline_query.query.strip()
    if not query:
        return

    results = []
    async with async_session_factory() as session:
        stmt = (
            select(Movie)
            .where(
                (Movie.name_ru.ilike(f"%{query}%"))
                | (Movie.name_original.ilike(f"%{query}%"))
            )
            .limit(10)
        )
        res = await session.execute(stmt)
        movies = res.scalars().all()

        for m in movies:
            title = m.name_ru or m.name_original or "Без названия"
            desc = f"{m.year or ''} | КП: {m.rating_kinopoisk or '—'} | {', '.join(m.genres[:2])}"
            caption = format_movie_caption(m)
            results.append(
                InlineQueryResultArticle(
                    id=str(m.id),
                    title=f"{title} ({m.year or '—'})",
                    description=desc,
                    thumbnail_url=m.poster_url_preview or m.poster_url,
                    input_message_content=InputTextMessageContent(
                        message_text=caption,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=False,
                    ),
                )
            )

    await update.inline_query.answer(results, cache_time=30)

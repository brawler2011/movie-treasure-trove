import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from sqlalchemy import func, select

from database.session import async_session_factory
from database.crud import (
    ensure_user,
    get_user_interactions,
    record_interaction,
    remove_from_watchlist,
)
from database.models import Movie, UserInteraction
from bot_features.card_builder import format_movie_caption
from bot_features.keyboards import (
    get_lists_menu_keyboard,
    get_list_item_keyboard,
    get_main_menu_keyboard,
)
from recommendation.engine import get_recommendation_engine

logger = logging.getLogger(__name__)


async def lists_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /lists или кнопки '🗂️ Мои списки'"""
    user = update.effective_user
    if not user:
        return

    async with async_session_factory() as session:
        await ensure_user(
            session,
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

        # Считаем количество в списках
        w_stmt = select(func.count(UserInteraction.id)).where(
            UserInteraction.telegram_id == user.id,
            UserInteraction.action == "WATCHLIST",
        )
        l_stmt = select(func.count(UserInteraction.id)).where(
            UserInteraction.telegram_id == user.id,
            UserInteraction.action == "LIKE",
        )
        w_cnt = (await session.execute(w_stmt)).scalar() or 0
        l_cnt = (await session.execute(l_stmt)).scalar() or 0

    text = (
        "🗂️ <b>Твои персональные списки:</b>\n\n"
        f"⏳ <b>Буду смотреть:</b> {w_cnt} шт.\n"
        f"❤️ <b>Понравившиеся:</b> {l_cnt} шт.\n\n"
        "Выбери список для просмотра:"
    )

    keyboard = get_lists_menu_keyboard(watchlist_count=w_cnt, liked_count=l_cnt)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=keyboard
        )


async def handle_list_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Просмотр конкретного списка (list_view_{ACTION}_{INDEX})"""
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()

    parts = query.data.split("_")
    action = parts[2]  # 'WATCHLIST' or 'LIKE'
    idx = int(parts[3])

    user = update.effective_user
    if not user:
        return

    async with async_session_factory() as session:
        movies = await get_user_interactions(
            session, telegram_id=user.id, action=action, limit=100
        )

    if not movies:
        list_name = (
            "«Буду смотреть»" if action == "WATCHLIST" else "«Понравившиеся»"
        )
        await query.message.reply_text(
            f"Список {list_name} пока пуст! Добавляй фильмы из рекомендаций или поиска.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard(),
        )
        return

    idx = max(0, min(idx, len(movies) - 1))
    movie = movies[idx]

    caption = (
        f"🗂️ <b>Список: {'⏳ Буду смотреть' if action == 'WATCHLIST' else '❤️ Понравившиеся'}</b>\n\n"
        + format_movie_caption(movie)
    )
    keyboard = get_list_item_keyboard(
        movie.id, action=action, current_idx=idx, total_count=len(movies)
    )

    poster = movie.poster_url_preview or movie.poster_url
    try:
        if poster:
            await query.message.reply_photo(
                photo=poster,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )
        else:
            await query.message.reply_text(
                caption, parse_mode=ParseMode.HTML, reply_markup=keyboard
            )
    except Exception:
        await query.message.reply_text(
            caption, parse_mode=ParseMode.HTML, reply_markup=keyboard
        )


async def handle_list_navigation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Навигация по элементам списка (list_nav_{ACTION}_{INDEX})"""
    await handle_list_view(update, context)


async def handle_list_delete(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Удаление фильма из списка (list_del_{MOVIE_ID}_{CURRENT_INDEX})"""
    query = update.callback_query
    if not query or not query.data:
        return

    parts = query.data.split("_")
    movie_id = int(parts[2])
    idx = int(parts[3])

    user = update.effective_user
    if not user:
        return

    async with async_session_factory() as session:
        await remove_from_watchlist(session, telegram_id=user.id, movie_id=movie_id)
        await session.commit()

    await query.answer("🗑️ Фильм удален из списка!")
    try:
        await query.message.delete()
    except Exception:
        pass

    # Обновляем просмотр списка
    context.user_data["current_list_idx"] = max(0, idx - 1)
    await lists_command(update, context)


async def handle_list_like(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Перенос фильма из 'Буду смотреть' в 'Понравившиеся' (list_like_{MOVIE_ID})"""
    query = update.callback_query
    if not query or not query.data:
        return

    parts = query.data.split("_")
    movie_id = int(parts[2])

    user = update.effective_user
    if not user:
        return

    async with async_session_factory() as session:
        await remove_from_watchlist(session, telegram_id=user.id, movie_id=movie_id)
        await record_interaction(session, user.id, movie_id, "LIKE")
        await session.commit()

    await query.answer("❤️ Отлично! Фильм перемещен в понравившиеся, вкусы обновлены.")
    rec_engine = get_recommendation_engine()
    await rec_engine.update_user_taste_vector(user.id)

    try:
        await query.message.delete()
    except Exception:
        pass

    await lists_command(update, context)

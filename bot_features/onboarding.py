import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from sqlalchemy import select

from database.session import async_session_factory
from database.crud import ensure_user, record_interaction
from database.models import Movie, UserInteraction
from bot_features.card_builder import format_movie_caption
from bot_features.keyboards import (
    get_main_menu_keyboard,
    get_blitz_keyboard,
)
from recommendation.engine import get_recommendation_engine

logger = logging.getLogger(__name__)

# Список культовых разноплановых фильмов для блица
BLITZ_FILM_TITLES = [
    "Интерстеллар",
    "Зеленая миля",
    "1+1",
    "Бойцовский клуб",
    "Темный рыцарь",
    "Унесенные призраками",
]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
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

        # Проверим, есть ли у пользователя уже оценки
        stmt = select(UserInteraction).where(UserInteraction.telegram_id == user.id)
        res = await session.execute(stmt)
        has_interactions = res.first() is not None

    welcome_text = (
        f"👋 <b>Привет, {user.first_name or 'киноман'}!</b>\n\n"
        "Я — умный рекомендательный бот фильмов на базе <b>локального AI-векторного поиска</b> и базы Кинопоиска 🎬\n\n"
        "✨ <b>Как я работаю:</b>\n"
        "1. Ты оцениваешь фильмы (❤️ нравится, 👎 не моё).\n"
        "2. Я в реальном времени анализирую сюжетные темы, жанры и атмосферу.\n"
        "3. Алгоритм непрерывно дообучается под твои вкусы и предлагает ленту рекомендаций!\n\n"
    )

    if has_interactions:
        welcome_text += (
            "У тебя уже есть сохраненные оценки! Можешь сразу нажать <b>🎬 Рекомендовать</b> "
            "или найти конкретный фильм через поиск."
        )
    else:
        welcome_text += (
            "🎯 <b>Давай быстро откалибруем твои вкусы!</b>\n"
            "Пройди короткий блиц из 5–6 культовых картин, либо найди любимые фильмы через поиск."
        )

    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard(),
    )

    if not has_interactions:
        await start_blitz(update, context)


async def start_blitz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запуск блиц-тестирования вкусов"""
    context.user_data["blitz_index"] = 0
    await show_blitz_card(update, context, index=0)


async def show_blitz_card(
    update: Update, context: ContextTypes.DEFAULT_TYPE, index: int
) -> None:
    """Показывает карточку фильма в блиц-режиме"""
    if index >= len(BLITZ_FILM_TITLES):
        await finish_blitz(update, context)
        return

    target_title = BLITZ_FILM_TITLES[index]
    async with async_session_factory() as session:
        stmt = select(Movie).where(Movie.name_ru.ilike(f"%{target_title}%"))
        res = await session.execute(stmt)
        movie = res.scalars().first()

    if not movie:
        # Если фильм не найден, переходим к следующему
        await show_blitz_card(update, context, index + 1)
        return

    caption = (
        f"⚡ <b>Калибровка вкусов ({index + 1}/{len(BLITZ_FILM_TITLES)})</b>\n\n"
        + format_movie_caption(movie, max_length=800)
    )
    keyboard = get_blitz_keyboard(
        movie.id, current_index=index, total_count=len(BLITZ_FILM_TITLES)
    )

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        try:
            if movie.poster_url_preview or movie.poster_url:
                await query.message.reply_photo(
                    photo=movie.poster_url_preview or movie.poster_url,
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
    else:
        try:
            if movie.poster_url_preview or movie.poster_url:
                await update.message.reply_photo(
                    photo=movie.poster_url_preview or movie.poster_url,
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


async def handle_blitz_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает нажатия в блиц-режиме (blitz_like_..., blitz_dislike_..., blitz_skip_...)"""
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()

    parts = query.data.split("_")
    # blitz_like_123_0
    action_type = parts[1]  # 'like', 'dislike', 'skip'
    movie_id = int(parts[2])
    current_index = int(parts[3])

    user = update.effective_user
    if not user:
        return

    # Записываем действие
    if action_type in ["like", "dislike"]:
        act = "LIKE" if action_type == "like" else "DISLIKE"
        async with async_session_factory() as session:
            await record_interaction(session, user.id, movie_id, act)
            await session.commit()

    # Удаляем или скрываем старую клавиатуру блица
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    # Переходим к следующему фильму блица
    await show_blitz_card(update, context, index=current_index + 1)


async def finish_blitz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Завершение блиц-теста вкусов и переход к рекомендациям"""
    user = update.effective_user
    if not user:
        return

    # Пересчитываем вектор вкуса
    rec_engine = get_recommendation_engine()
    await rec_engine.update_user_taste_vector(user.id)

    text = (
        "🎉 <b>Калибровка успешно завершена!</b>\n\n"
        "Твой начальный профиль вкусов построен. Теперь нейросетевой алгоритм готов подбирать персональные фильмы.\n"
        "Жми <b>🎬 Начать рекомендации</b> ниже!"
    )

    # Импортируем функцию запуска ленты
    from bot_features.feed import send_next_recommendation

    if update.callback_query:
        await update.callback_query.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=get_main_menu_keyboard()
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=get_main_menu_keyboard()
        )

    # Автоматически отправляем первую персональную рекомендацию
    await send_next_recommendation(update, context)

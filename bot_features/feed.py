import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from database.session import async_session_factory
from database.crud import ensure_user, record_interaction
from bot_features.card_builder import format_movie_caption
from bot_features.keyboards import get_rec_card_keyboard, get_main_menu_keyboard
from recommendation.engine import get_recommendation_engine

logger = logging.getLogger(__name__)


async def recommend_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /recommend или нажатия кнопки '🎬 Рекомендовать'"""
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

    await send_next_recommendation(update, context)


async def send_next_recommendation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Подбирает и отправляет следующую лучшую рекомендацию"""
    user = update.effective_user
    if not user:
        return

    rec_engine = get_recommendation_engine()
    genre_filter = context.user_data.get("active_genre")
    type_filter = context.user_data.get("active_type")

    # Получаем рекомендацию
    recs = await rec_engine.get_recommendations(
        telegram_id=user.id,
        limit=1,
        genre_filter=genre_filter,
        type_filter=type_filter,
    )

    if not recs:
        text = (
            "🍿 <b>Кажется, подходящие фильмы по текущим фильтрам закончились!</b>\n\n"
            "Попробуй сбросить жанровый фильтр через меню <b>⚙️ Фильтры</b> "
            "или найди любой новый фильм через <b>🔍 Поиск</b>, чтобы расширить базу."
        )
        if update.callback_query:
            await update.callback_query.message.reply_text(
                text, parse_mode=ParseMode.HTML, reply_markup=get_main_menu_keyboard()
            )
        else:
            await update.message.reply_text(
                text, parse_mode=ParseMode.HTML, reply_markup=get_main_menu_keyboard()
            )
        return

    movie = recs[0]
    caption = format_movie_caption(movie)
    keyboard = get_rec_card_keyboard(movie.id, current_genre=genre_filter)

    poster = movie.poster_url_preview or movie.poster_url

    if update.callback_query:
        query = update.callback_query
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
    else:
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


async def handle_feed_reaction(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Обрабатывает реакции на карточку фильма:
    feed_like_<id>, feed_dislike_<id>, feed_watch_<id>, feed_skip_<id>
    """
    query = update.callback_query
    if not query or not query.data:
        return

    parts = query.data.split("_")
    action_type = parts[1]  # like, dislike, watch, skip
    movie_id = int(parts[2])

    user = update.effective_user
    if not user:
        return

    rec_engine = get_recommendation_engine()

    if action_type == "like":
        async with async_session_factory() as session:
            await record_interaction(session, user.id, movie_id, "LIKE")
            await session.commit()
        await query.answer("❤️ Добавлено в понравившиеся! Вкусы обновлены.")
        # Обновляем вектор вкуса
        await rec_engine.update_user_taste_vector(user.id)

    elif action_type == "dislike":
        async with async_session_factory() as session:
            await record_interaction(session, user.id, movie_id, "DISLIKE")
            await session.commit()
        await query.answer("👎 Понял, убираю этот стиль из рекомендаций.")
        # Обновляем вектор вкуса
        await rec_engine.update_user_taste_vector(user.id)

    elif action_type == "watch":
        async with async_session_factory() as session:
            await record_interaction(session, user.id, movie_id, "WATCHLIST")
            await session.commit()
        await query.answer("⏳ Фильм сохранен в список 'Буду смотреть'!")

    elif action_type == "skip":
        async with async_session_factory() as session:
            await record_interaction(session, user.id, movie_id, "SKIP")
            await session.commit()
        await query.answer("➡️ Пропущено.")

    # Удаляем клавиатуру у старого сообщения
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    # Отправляем следующий фильм
    await send_next_recommendation(update, context)

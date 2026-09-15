import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from database.session import async_session_factory
from database.crud import (
    ensure_user,
    get_user_reaction,
    record_interaction,
    set_or_toggle_interaction,
)
from bot_features.card_builder import format_movie_caption, ensure_movie_description
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
    async with async_session_factory() as session:
        await ensure_movie_description(movie, session=session)
        user_reaction = await get_user_reaction(session, user.id, movie.id)
    caption = format_movie_caption(movie)
    keyboard = get_rec_card_keyboard(
        movie.id, current_genre=genre_filter, user_reaction=user_reaction
    )

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
    genre_filter = context.user_data.get("active_genre")

    if action_type == "skip":
        async with async_session_factory() as session:
            await record_interaction(session, user.id, movie_id, "SKIP")
            await session.commit()
        await query.answer("➡️ Пропущено.")
        # Обновляем клавиатуру у текущего сообщения
        try:
            keyboard = get_rec_card_keyboard(
                movie_id, current_genre=genre_filter, user_reaction="SKIP"
            )
            await query.edit_message_reply_markup(reply_markup=keyboard)
        except Exception:
            pass
        # Отправляем следующий фильм
        await send_next_recommendation(update, context)
        return

    action_map = {
        "like": "LIKE",
        "dislike": "DISLIKE",
        "watch": "WATCHLIST",
    }
    target_action = action_map.get(action_type)
    if not target_action:
        return

    async with async_session_factory() as session:
        current_reaction, is_toggled_off, previous_reaction = (
            await set_or_toggle_interaction(session, user.id, movie_id, target_action)
        )
        await session.commit()

    # Обновляем вектор вкусов пользователя при затрагивании LIKE или DISLIKE
    if target_action in ("LIKE", "DISLIKE") or previous_reaction in ("LIKE", "DISLIKE"):
        await rec_engine.update_user_taste_vector(user.id)

    # Обновляем клавиатуру на текущей карточке с отображением актуального выбора
    try:
        updated_keyboard = get_rec_card_keyboard(
            movie_id, current_genre=genre_filter, user_reaction=current_reaction
        )
        await query.edit_message_reply_markup(reply_markup=updated_keyboard)
    except Exception as e:
        logger.debug("Не удалось обновить клавиатуру сообщения: %s", e)

    # 1. Если реакция была снята повторным нажатием (Toggle OFF)
    if is_toggled_off:
        await query.answer("Реакция снята.")
        return

    # 2. Если реакция была изменена на ранее оцененной карточке
    if previous_reaction is not None:
        action_names = {
            "LIKE": "«Нравится»",
            "DISLIKE": "«Не моё»",
            "WATCHLIST": "«Буду смотреть»",
        }
        await query.answer(
            f"Реакция изменена на {action_names.get(current_reaction, '')}!"
        )
        return

    # 3. Реакция установлена впервые на свежей карточке
    if current_reaction == "LIKE":
        await query.answer("❤️ Добавлено в понравившиеся! Вкусы обновлены.")
    elif current_reaction == "DISLIKE":
        await query.answer("👎 Понял, убираю этот стиль из рекомендаций.")
    elif current_reaction == "WATCHLIST":
        await query.answer("⏳ Фильм сохранен в список 'Буду смотреть'!")

    # Отправляем следующий фильм
    await send_next_recommendation(update, context)

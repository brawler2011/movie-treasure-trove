import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot_features.keyboards import (
    get_genre_filter_keyboard,
    get_type_filter_keyboard,
    get_main_menu_keyboard,
)

logger = logging.getLogger(__name__)


async def filter_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /filter или кнопки '⚙️ Фильтры'"""
    active_genre = context.user_data.get("active_genre")
    active_type = context.user_data.get("active_type")

    genre_str = active_genre.capitalize() if active_genre else "Любой (все)"
    type_str = (
        "🎬 Только фильмы"
        if active_type == "FILM"
        else ("📺 Только сериалы" if active_type == "TV_SERIES" else "Любой")
    )

    text = (
        "⚙️ <b>Настройка фильтров под настроение:</b>\n\n"
        f"🎭 <b>Текущий жанр:</b> <code>{genre_str}</code>\n"
        f"📽️ <b>Тип контента:</b> <code>{type_str}</code>\n\n"
        "Выбери жанр для рекомендаций ниже:"
    )

    keyboard = get_genre_filter_keyboard(
        active_genre=active_genre, active_type=active_type
    )

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=keyboard
        )


async def handle_set_genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Установка фильтра по жанру (set_genre_{GENRE})"""
    query = update.callback_query
    if not query or not query.data:
        return

    genre = query.data.replace("set_genre_", "")
    context.user_data["active_genre"] = genre
    await query.answer(f"✅ Фильтр установлен: {genre.capitalize()}")

    # Обновляем сообщение с клавиатурой
    await filter_command(update, context)


async def handle_reset_genre(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Сброс всех фильтров (жанр и тип)"""
    query = update.callback_query
    if not query:
        return

    context.user_data["active_genre"] = None
    context.user_data["active_type"] = None
    await query.answer("❌ Фильтры сброшены")
    await filter_command(update, context)


async def handle_set_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Установка типа (FILM / TV_SERIES)"""
    query = update.callback_query
    if not query or not query.data:
        return

    ctype = query.data.replace("set_type_", "")
    context.user_data["active_type"] = ctype
    await query.answer(f"✅ Тип установлен: {ctype}")
    await filter_command(update, context)


async def handle_reset_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Сброс фильтра типа"""
    query = update.callback_query
    if not query:
        return

    context.user_data["active_type"] = None
    await query.answer("❌ Фильтр типа сброшен")
    await filter_command(update, context)

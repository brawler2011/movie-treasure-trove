from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot_features.keyboards import get_main_menu_keyboard


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Справка по командам и работе бота"""
    help_text = (
        "📖 <b>Справка по использованию бота:</b>\n\n"
        "⚡ <b>Команды:</b>\n"
        "• /start — Запуск бота и калибровка вкусов\n"
        "• /recommend — Получить персональную рекомендацию\n"
        "• /search — Поиск фильма по названию\n"
        "• /lists — Списки «Буду смотреть» и «Понравившиеся»\n"
        "• /filter — Фильтры по жанру и типу контента\n"
        "• /help — Данное справочное меню\n\n"
        "🎬 <b>Управление карточкой фильма:</b>\n"
        "• <b>❤️ Нравится</b> — добавляет фильм в любимые и сдвигает вектор вкусов в сторону его жанров и сюжета.\n"
        "• <b>👎 Не моё</b> — обучает алгоритм избегать подобных фильмов.\n"
        "• <b>⏳ Буду смотреть</b> — сохраняет фильм в личный список просмотра.\n"
        "• <b>➡️ Дальше</b> — переход к следующей картине без влияния на вектор вкусов.\n\n"
        "💡 <i>Совет: ты можешь в любой момент написать название любого фильма текстом в чат, чтобы найти его и оценить!</i>"
    )

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            help_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard(),
        )
    else:
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard(),
        )

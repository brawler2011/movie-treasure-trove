import asyncio
import logging
import os
import sys

# Понижаем приоритет процесса для планировщика Linux (nice 10),
# чтобы системные службы (sshd, systemd, сеть) гарантированно получали CPU на слабых VPS
try:
    os.nice(10)
except Exception:
    pass

from telegram import MenuButtonWebApp, Update, WebAppInfo
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    InlineQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import uvicorn

from config import (
    API_HOST,
    API_PORT,
    BOT_TOKEN,
    RUN_VITE,
    TELEGRAM_CONCURRENT_UPDATES,
    WEBAPP_PORT,
    WEBAPP_URL,
)
from database import init_db
from recommendation.engine import get_recommendation_engine
from webapp_api.server import create_app
from bot_features.onboarding import (
    start_command,
    start_blitz,
    handle_blitz_callback,
)
from bot_features.feed import (
    recommend_command,
    send_next_recommendation,
    handle_feed_reaction,
)
from bot_features.search import (
    search_command,
    handle_search_query,
    handle_search_reaction,
    inline_search,
)
from bot_features.lists import (
    lists_command,
    handle_list_view,
    handle_list_navigation,
    handle_list_delete,
    handle_list_like,
)
from bot_features.filter import (
    filter_command,
    handle_set_genre,
    handle_reset_genre,
    handle_set_type,
    handle_reset_type,
)
from bot_features.help import help_command

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("movie_bot")


async def handle_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Диспетчер текстовых сообщений (кнопки меню или поиск фильмов)"""
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    if text == "🎬 Рекомендовать":
        await recommend_command(update, context)
    elif text == "🔍 Поиск":
        await search_command(update, context)
    elif text == "🗂️ Мои списки":
        await lists_command(update, context)
    elif text == "⚙️ Фильтры":
        await filter_command(update, context)
    elif text == "⚡ Пройти блиц-тест вкусов":
        await start_blitz(update, context)
    else:
        # Считаем сообщение поисковым запросом названия фильма
        await handle_search_query(update, context)


async def post_init(application: Application) -> None:
    """Инициализация базы данных, рекомендательного движка, кнопки меню и сервера FastAPI"""
    logger.info("Инициализация базы данных...")
    await init_db()
    logger.info("Загрузка векторного кэша рекомендательного движка...")
    engine = get_recommendation_engine()
    await engine.ensure_initialized()

    # Настраиваем системную кнопку меню Telegram WebApp (слева от поля ввода)
    try:
        await application.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🎬 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        )
        logger.info("Кнопка меню Telegram успешно установлена: %s", WEBAPP_URL)
    except Exception as e:
        logger.warning("Не удалось настроить MenuButtonWebApp (возможно, оффлайн): %s", e)

    # Запускаем встроенный FastAPI веб-сервер в едином event loop
    fastapi_app = create_app()
    uvicorn_config = uvicorn.Config(
        app=fastapi_app,
        host=API_HOST,
        port=API_PORT,
        log_level="info",
        access_log=False,
    )
    server = uvicorn.Server(uvicorn_config)
    application.bot_data["uvicorn_server"] = server
    application.bot_data["uvicorn_task"] = asyncio.create_task(server.serve())
    logger.info(
        "Бэкенд API запущен на http://%s:%s",
        API_HOST,
        API_PORT,
    )

    # Опциональный автоматический запуск Vite сервера статики (если RUN_VITE=true)
    if RUN_VITE:
        webapp_dir = os.path.join(os.path.dirname(__file__), "webapp")
        if os.path.isdir(webapp_dir):
            logger.info("Запуск Vite сервера статики на порту %s...", WEBAPP_PORT)
            env = os.environ.copy()
            env["PORT"] = str(WEBAPP_PORT)
            env["API_TARGET"] = f"http://127.0.0.1:{API_PORT}"
            proc = await asyncio.create_subprocess_exec(
                "npm", "run", "serve",
                cwd=webapp_dir,
                env=env,
            )
            application.bot_data["vite_proc"] = proc
            logger.info("Vite сервер запущен (PID %s) на порту %s", proc.pid, WEBAPP_PORT)

    logger.info("Бот и WebApp полностью готовы к обработке запросов!")


async def post_shutdown(application: Application) -> None:
    """Корректная остановка серверов при выключении бота"""
    vite_proc = application.bot_data.get("vite_proc")
    if vite_proc:
        logger.info("Остановка Vite сервера...")
        try:
            vite_proc.terminate()
            await vite_proc.wait()
        except Exception:
            pass

    server = application.bot_data.get("uvicorn_server")
    if server:
        logger.info("Остановка веб-сервера FastAPI...")
        server.should_exit = True
        task = application.bot_data.get("uvicorn_task")
        if task:
            try:
                await task
            except Exception:
                pass


def main() -> None:
    if not BOT_TOKEN:
        print("\n" + "=" * 60)
        print(" ОШИБКА: BOT_TOKEN не задан в .env или переменных окружения!")
        print(" Пожалуйста, укажите токен Telegram-бота от @BotFather в файле .env:")
        print(" BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        print("=" * 60 + "\n")
        sys.exit(1)

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(TELEGRAM_CONCURRENT_UPDATES)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    # 1. Команды пользователя
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("recommend", recommend_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("lists", lists_command))
    application.add_handler(CommandHandler("filter", filter_command))
    application.add_handler(CommandHandler("help", help_command))

    # 2. Инлайн-поиск в любых чатах
    application.add_handler(InlineQueryHandler(inline_search))

    # 3. Инлайн-кнопки (Callback Queries)
    # Блиц-онбординг
    application.add_handler(CallbackQueryHandler(handle_blitz_callback, pattern=r"^blitz_"))

    # Лента рекомендаций
    application.add_handler(CallbackQueryHandler(handle_feed_reaction, pattern=r"^feed_(like|dislike|watch|skip)_"))
    application.add_handler(CallbackQueryHandler(send_next_recommendation, pattern=r"^feed_start$"))

    # Поиск
    application.add_handler(CallbackQueryHandler(handle_search_reaction, pattern=r"^search_(like|watch)_"))

    # Списки
    application.add_handler(CallbackQueryHandler(handle_list_view, pattern=r"^list_view_"))
    application.add_handler(CallbackQueryHandler(handle_list_navigation, pattern=r"^list_nav_"))
    application.add_handler(CallbackQueryHandler(handle_list_delete, pattern=r"^list_del_"))
    application.add_handler(CallbackQueryHandler(handle_list_like, pattern=r"^list_like_"))
    application.add_handler(CallbackQueryHandler(lists_command, pattern=r"^menu_lists$"))

    # Фильтры
    application.add_handler(CallbackQueryHandler(handle_set_genre, pattern=r"^set_genre_"))
    application.add_handler(CallbackQueryHandler(handle_reset_genre, pattern=r"^reset_genre$"))
    application.add_handler(CallbackQueryHandler(handle_set_type, pattern=r"^set_type_"))
    application.add_handler(CallbackQueryHandler(handle_reset_type, pattern=r"^reset_type$"))
    application.add_handler(CallbackQueryHandler(filter_command, pattern=r"^menu_filter_genre$"))

    # 4. Текстовые сообщения
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)
    )

    logger.info("Запуск Telegram-бота (polling)...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

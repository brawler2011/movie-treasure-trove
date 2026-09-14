import argparse
import asyncio
import logging
import os
import sys
import time
from typing import List, Optional

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden, RetryAfter, TelegramError

from config import BOT_TOKEN, WEBAPP_URL
from database.models import User
from database.session import get_session

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("broadcast")

DEFAULT_MESSAGE = (
    "🍿 <b>Встречайте мини-приложение «Кинокладезь»!</b>\n\n"
    "Теперь выбирать фильмы и управлять списками стало ещё удобнее "
    "в новом интерактивном формате.\n\n"
    "Нажмите кнопку ниже, чтобы запустить приложение прямо в Telegram! 👇"
)

DEFAULT_BUTTON_TEXT = "📱 Запустить приложение"


def build_keyboard(button_text: str, webapp_url: str) -> InlineKeyboardMarkup:
    """Создаёт инлайн-кнопку для запуска WebApp внутри Telegram"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=button_text,
                    web_app=WebAppInfo(url=webapp_url),
                )
            ]
        ]
    )


async def send_notification_to_user(
    bot: Bot,
    chat_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup,
) -> bool:
    """
    Отправляет уведомление конкретному пользователю с обработкой исключений и флуд-лимитов.
    Возвращает True в случае успеха, False при ошибке/блокировке.
    """
    max_retries = 2
    for attempt in range(max_retries):
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
            )
            logger.info("Успешно отправлено пользователю chat_id=%s", chat_id)
            return True
        except RetryAfter as e:
            wait_time = int(e.retry_after) + 1
            logger.warning(
                "Превышен лимит Telegram (FloodWait). Ожидание %s сек перед повтором для %s...",
                wait_time,
                chat_id,
            )
            await asyncio.sleep(wait_time)
        except Forbidden as e:
            logger.warning("Пользователь chat_id=%s заблокировал бота: %s", chat_id, e)
            return False
        except BadRequest as e:
            logger.warning("Ошибка BadRequest для chat_id=%s (чат не найден/удалён): %s", chat_id, e)
            return False
        except TelegramError as e:
            logger.error("Ошибка Telegram API при отправке %s (попытка %d): %s", chat_id, attempt + 1, e)
            if attempt < max_retries - 1:
                await asyncio.sleep(1.0)
            else:
                return False
        except Exception as e:
            logger.exception("Непредвиденная ошибка при отправке пользователю %s: %s", chat_id, e)
            return False
    return False


async def fetch_all_users() -> List[User]:
    """Получает список всех зарегистрированных пользователей из базы данных"""
    async with get_session() as session:
        stmt = select(User).order_by(User.created_at.desc())
        res = await session.execute(stmt)
        return list(res.scalars().all())


async def run_broadcast(
    test_chat_id: Optional[int] = None,
    send_all: bool = False,
    dry_run: bool = False,
    delay: float = 0.05,
    message_text: str = DEFAULT_MESSAGE,
    button_text: str = DEFAULT_BUTTON_TEXT,
    webapp_url: str = WEBAPP_URL,
):
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не задан в конфигурации или .env!")
        return

    logger.info("=== Запуск скрипта рассылки ===")
    logger.info("URL WebApp: %s", webapp_url)
    logger.info("Кнопка: [%s]", button_text)
    logger.info("Текст сообщения:\n%s\n%s", "-" * 40, message_text)
    logger.info("-" * 40)

    keyboard = build_keyboard(button_text, webapp_url)

    # 1. Тестовая отправка на конкретный chat_id
    if test_chat_id:
        logger.info("Запуск ТЕСТОВОЙ отправки на chat_id=%s...", test_chat_id)
        if dry_run:
            logger.info("[DRY-RUN] Тестовое сообщение НЕ отправлено, режим симуляции.")
            return

        bot = Bot(token=BOT_TOKEN)
        async with bot:
            success = await send_notification_to_user(bot, test_chat_id, message_text, keyboard)
        if success:
            logger.info("✅ Тестовое сообщение успешно доставлено на chat_id=%s!", test_chat_id)
        else:
            logger.error("❌ Не удалось доставить тестовое сообщение на chat_id=%s.", test_chat_id)
        return

    # 2. Рассылка всем пользователям из базы
    users = await fetch_all_users()
    logger.info("Найдено пользователей в базе: %d", len(users))

    if not users:
        logger.warning("В базе данных нет пользователей для рассылки.")
        return

    for u in users:
        logger.info("  - ID: %s, username: @%s, имя: %s", u.telegram_id, u.username, u.first_name)

    if dry_run or not send_all:
        logger.info("[DRY-RUN / ПРЕДПРОСМОТР] Сообщения НЕ отправлялись.")
        logger.info("Для реальной массовой отправки запустите скрипт с флагом --send-all.")
        return

    logger.info("Начало массовой рассылки (задержка между сообщениями: %.3f с)...", delay)
    start_time = time.time()
    successful = 0
    failed = 0

    bot = Bot(token=BOT_TOKEN)
    async with bot:
        for idx, user in enumerate(users, start=1):
            logger.info("[%d/%d] Отправка пользователю %s...", idx, len(users), user.telegram_id)
            ok = await send_notification_to_user(bot, user.telegram_id, message_text, keyboard)
            if ok:
                successful += 1
            else:
                failed += 1

            if delay > 0:
                await asyncio.sleep(delay)

    total_time = time.time() - start_time
    logger.info("=== Итоги рассылки ===")
    logger.info("Всего пользователей: %d", len(users))
    logger.info("Успешно доставлено: %d", successful)
    logger.info("Ошибок / заблокировано: %d", failed)
    logger.info("Затраченное время: %.2f сек", total_time)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Скрипт рассылки уведомления о Mini App пользователям Telegram-бота."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--test",
        type=int,
        metavar="CHAT_ID",
        help="Отправить тестовое уведомление на указанный Telegram chat_id",
    )
    group.add_argument(
        "--send-all",
        action="store_true",
        help="Запустить массовую рассылку всем пользователям из базы данных",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Вывести список пользователей и сообщение без реальной отправки",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.05,
        help="Задержка в секундах между отправками (по умолчанию 0.05с для безопасного rate limit)",
    )
    parser.add_argument(
        "--message",
        type=str,
        default=DEFAULT_MESSAGE,
        help="Пользовательский текст сообщения (поддерживает HTML)",
    )
    parser.add_argument(
        "--button-text",
        type=str,
        default=DEFAULT_BUTTON_TEXT,
        help="Текст инлайн-кнопки",
    )
    parser.add_argument(
        "--webapp-url",
        type=str,
        default=WEBAPP_URL,
        help="URL Mini App для кнопки",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    asyncio.run(
        run_broadcast(
            test_chat_id=args.test,
            send_all=args.send_all,
            dry_run=args.dry_run,
            delay=args.delay,
            message_text=args.message,
            button_text=args.button_text,
            webapp_url=args.webapp_url,
        )
    )


if __name__ == "__main__":
    main()

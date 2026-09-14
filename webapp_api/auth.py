import hashlib
import hmac
import json
import logging
import urllib.parse
from typing import Any, Dict, Optional

from fastapi import Header, Query

from config import BOT_TOKEN

logger = logging.getLogger(__name__)


def validate_telegram_data(init_data: str, bot_token: str) -> Optional[Dict[str, Any]]:
    """
    Проверяет валидность строки initData от Telegram WebApp по официальному алгоритму HMAC-SHA256.
    Возвращает словарь данных (включая распарсенный объект user) или None, если подпись неверна.
    """
    if not init_data or not bot_token:
        return None

    try:
        parsed = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
        received_hash = parsed.pop("hash", None)
        if not received_hash:
            return None

        # Сортируем пары по алфавиту ключей
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))

        # secret_key = HMAC_SHA256("WebAppData", bot_token)
        secret_key = hmac.new(
            b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256
        ).digest()

        # calculated_hash = HMAC_SHA256(secret_key, data_check_string)
        calculated_hash = hmac.new(
            secret_key, data_check_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(calculated_hash, received_hash):
            if "user" in parsed:
                try:
                    parsed["user"] = json.loads(parsed["user"])
                except Exception:
                    pass
            return parsed
        return None
    except Exception as e:
        logger.warning("Ошибка проверки Telegram initData: %s", e)
        return None


async def get_current_user_tg(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    tg_init_data: Optional[str] = Query(None, alias="initData"),
) -> Dict[str, Any]:
    """
    Зависимость FastAPI для извлечения пользователя Telegram.
    Проверяет initData из заголовка X-Telegram-Init-Data, Authorization (tma <initData>) или query-параметра.
    Для удобства локальной разработки вне Telegram поддерживается mock-пользователь.
    """
    raw_init_data = x_telegram_init_data or tg_init_data

    if not raw_init_data and authorization:
        if authorization.startswith("tma "):
            raw_init_data = authorization[4:].strip()
        elif authorization.startswith("Bearer "):
            raw_init_data = authorization[7:].strip()

    if raw_init_data:
        data = validate_telegram_data(raw_init_data, BOT_TOKEN)
        if data and "user" in data:
            user_data = data["user"]
            if isinstance(user_data, dict) and "id" in user_data:
                return {
                    "telegram_id": int(user_data["id"]),
                    "username": user_data.get("username"),
                    "first_name": user_data.get("first_name", "Гость"),
                    "is_premium": user_data.get("is_premium", False),
                }

    # Если мы запускаем в браузере для тестов и нет initData:
    # Используем дефолтный тестовый аккаунт, чтобы интерфейс открывался в обычном браузере
    return {
        "telegram_id": 999999999,
        "username": "browser_guest",
        "first_name": "Киноман",
        "is_premium": False,
        "is_dev": True,
    }

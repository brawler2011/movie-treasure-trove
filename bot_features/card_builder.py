import logging
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import InlineKeyboardMarkup
from database.models import Movie
from kp_sdk.client import KinopoiskSDK

logger = logging.getLogger(__name__)


async def ensure_movie_description(
    movie: Movie, session: Optional[AsyncSession] = None
) -> Movie:
    """
    Проверяет наличие описания у фильма. Если описание отсутствует в БД,
    подгружает его через Kinopoisk API и сохраняет в сессии.
    """
    if movie.description or movie.short_description:
        return movie

    if not movie.kinopoisk_id:
        return movie

    try:
        sdk = KinopoiskSDK()
        async with sdk:
            film_details = await sdk.get_film_details(movie.kinopoisk_id)
            if film_details:
                desc = getattr(film_details, "description", None)
                short_desc = getattr(film_details, "short_description", None)
                if desc:
                    movie.description = desc
                if short_desc:
                    movie.short_description = short_desc
                if not movie.film_length and getattr(film_details, "film_length", None):
                    movie.film_length = film_details.film_length
                if not movie.poster_url and getattr(film_details, "poster_url", None):
                    movie.poster_url = film_details.poster_url
                if not movie.poster_url_preview and getattr(
                    film_details, "poster_url_preview", None
                ):
                    movie.poster_url_preview = film_details.poster_url_preview
                if not movie.web_url and getattr(film_details, "web_url", None):
                    movie.web_url = film_details.web_url

                fd_type = getattr(film_details, "type_", getattr(film_details, "type", None))
                is_serial = getattr(film_details, "serial", None)
                if fd_type:
                    val = getattr(fd_type, "value", fd_type)
                    if val:
                        movie.type = str(val)
                elif is_serial:
                    movie.type = "TV_SERIES"

                if session:
                    session.add(movie)
                    await session.commit()
    except Exception as e:
        logger.warning(
            "Не удалось подгрузить описание для фильма %s (ID %s): %s",
            movie.name_ru,
            movie.kinopoisk_id,
            e,
        )

    return movie


def get_content_type_info(movie: Movie) -> Tuple[str, str, str]:
    """
    Возвращает (иконка, название_типа, метка_хронометража).
    Например: ("📺", "Сериал", "Серия:") или ("🎬", "Фильм", "Время:")
    """
    raw_type = (movie.type or "FILM").upper()
    if raw_type == "MINI_SERIES":
        return "📺", "Мини-сериал", "Серия:"
    elif raw_type in ("TV_SERIES", "TV_SHOW"):
        return "📺", "Сериал", "Серия:"
    else:
        return "🎬", "Фильм", "Время:"


def format_movie_caption(movie: Movie, max_length: int = 1000) -> str:
    """Форматирует красивую карточку фильма или сериала для отправки в Telegram"""
    title = movie.name_ru or movie.name_original or "Без названия"
    year_str = f" ({movie.year})" if movie.year else ""
    icon, type_label, length_label = get_content_type_info(movie)

    lines = [f"{icon} <b>{title}</b>{year_str}\n"]

    # Рейтинги
    ratings = []
    if movie.rating_kinopoisk:
        ratings.append(f"Кинопоиск: ⭐️ <b>{movie.rating_kinopoisk}</b>")
    if movie.rating_imdb:
        ratings.append(f"IMDb: <b>{movie.rating_imdb}</b>")
    if ratings:
        lines.append(" | ".join(ratings))

    # Тип контента (Фильм / Сериал)
    lines.append(f"📽️ Тип: <b>{type_label}</b>")

    # Жанры
    genres = movie.genres
    if genres:
        lines.append(f"🎭 Жанры: <i>{', '.join(genres)}</i>")

    # Страны
    countries = movie.countries
    if countries:
        lines.append(f"🌍 Страна: {', '.join(countries)}")

    # Хронометраж
    if movie.film_length:
        lines.append(f"⏱ {length_label} {movie.film_length} мин.")

    # Ссылки
    links = []
    if movie.web_url:
        links.append(f"🔗 <a href='{movie.web_url}'>Кинопоиск</a>")
    if movie.kinopoisk_id:
        links.append(
            f"🍿 <a href='https://www.kinopoisk.cx/film/{movie.kinopoisk_id}/'>Смотреть бесплатно</a>"
        )

    links_text = f"\n{' • '.join(links)}" if links else ""

    short_desc = (movie.short_description or "").strip()
    full_desc = (movie.description or "").strip()

    # Формируем блок описания
    desc_elements = []
    if short_desc and full_desc and short_desc.lower() not in full_desc.lower():
        desc_elements = ["", f"<i>«{short_desc}»</i>", "", f"📝 {full_desc}"]
    elif full_desc:
        desc_elements = ["", f"📝 {full_desc}"]
    elif short_desc:
        desc_elements = ["", f"📝 {short_desc}"]

    parts = list(lines) + desc_elements
    if links_text:
        parts.append(links_text)

    full_text = "\n".join(parts)

    # Если превышает max_length, сначала убираем слоган/цитату
    if len(full_text) > max_length and short_desc and full_desc:
        desc_elements = ["", f"📝 {full_desc}"]
        parts = list(lines) + desc_elements
        if links_text:
            parts.append(links_text)
        full_text = "\n".join(parts)

    # Если всё ещё превышает max_length, аккуратно обрезаем описание по границе слова
    if len(full_text) > max_length and (full_desc or short_desc):
        desc = full_desc or short_desc
        base_parts = list(lines)
        if links_text:
            base_parts.append(links_text)
        base_len = len("\n".join(base_parts)) + len("\n\n📝 ...")
        available_desc_len = max(50, max_length - base_len)
        truncated_desc = desc[:available_desc_len]
        last_space = truncated_desc.rfind(" ")
        if last_space > 30:
            truncated_desc = truncated_desc[:last_space]
        truncated_desc = truncated_desc.rstrip(" .,!?:;") + "..."

        parts = list(lines) + ["", f"📝 {truncated_desc}"]
        if links_text:
            parts.append(links_text)
        full_text = "\n".join(parts)

    return full_text

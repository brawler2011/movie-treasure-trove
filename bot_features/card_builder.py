from typing import Optional, Tuple
from telegram import InlineKeyboardMarkup
from database.models import Movie


def format_movie_caption(movie: Movie, max_length: int = 1000) -> str:
    """Форматирует красивую карточку фильма для отправки в Telegram"""
    title = movie.name_ru or movie.name_original or "Без названия"
    year_str = f" ({movie.year})" if movie.year else ""

    lines = [f"🎬 <b>{title}</b>{year_str}\n"]

    # Рейтинги
    ratings = []
    if movie.rating_kinopoisk:
        ratings.append(f"Кинопоиск: ⭐️ <b>{movie.rating_kinopoisk}</b>")
    if movie.rating_imdb:
        ratings.append(f"IMDb: <b>{movie.rating_imdb}</b>")
    if ratings:
        lines.append(" | ".join(ratings))

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
        lines.append(f"⏱ Время: {movie.film_length} мин.")

    # Ссылки
    links = []
    if movie.web_url:
        links.append(f"🔗 <a href='{movie.web_url}'>Кинопоиск</a>")
    if movie.kinopoisk_id:
        links.append(
            f"🍿 <a href='https://www.kinopoisk.cx/film/{movie.kinopoisk_id}/'>Смотреть бесплатно</a>"
        )

    links_text = f"\n{' • '.join(links)}" if links else ""

    desc = (movie.short_description or movie.description or "").strip()

    # Сборка без усечения
    parts = list(lines)
    if desc:
        parts.extend(["", f"📝 {desc}"])
    if links_text:
        parts.append(links_text)

    full_text = "\n".join(parts)
    if len(full_text) > max_length and desc:
        overflow = len(full_text) - max_length + 20
        truncated_desc = desc[:-overflow].strip() + "..."
        parts = list(lines)
        parts.extend(["", f"📝 {truncated_desc}"])
        if links_text:
            parts.append(links_text)
        full_text = "\n".join(parts)

    return full_text

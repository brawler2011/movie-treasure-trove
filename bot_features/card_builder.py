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

    lines.append("")  # пустая строка перед описанием

    # Описание
    desc = movie.short_description or movie.description or ""
    if desc:
        desc_clean = desc.strip()
        lines.append(f"📝 {desc_clean}")

    if movie.web_url:
        lines.append(f"\n🔗 <a href='{movie.web_url}'>Страница на Кинопоиске</a>")

    full_text = "\n".join(lines)
    if len(full_text) > max_length:
        # Усекаем описание, если превышен лимит
        overflow = len(full_text) - max_length + 20
        truncated_desc = desc[:-overflow].strip() + "..."
        # Пересобираем
        lines_truncated = lines[:-2] + [f"📝 {truncated_desc}"]
        if movie.web_url:
            lines_truncated.append(
                f"\n🔗 <a href='{movie.web_url}'>Страница на Кинопоиске</a>"
            )
        full_text = "\n".join(lines_truncated)

    return full_text

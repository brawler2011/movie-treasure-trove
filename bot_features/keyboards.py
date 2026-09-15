from typing import List, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from config import WEBAPP_URL

POPULAR_GENRES = [
    "фантастика",
    "боевик",
    "триллер",
    "драма",
    "комедия",
    "детектив",
    "криминал",
    "ужасы",
    "приключения",
    "фэнтези",
    "мелодрама",
    "мультфильм",
]


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура команд бота с кнопкой запуска WebApp"""
    webapp_btn = KeyboardButton("📱 Кино-Тиндер (Web App)", web_app=WebAppInfo(url=WEBAPP_URL))
    return ReplyKeyboardMarkup(
        [
            [webapp_btn],
            ["🎬 Рекомендовать", "🔍 Поиск"],
            ["🗂️ Мои списки", "⚙️ Фильтры"],
            ["⚡ Пройти блиц-тест вкусов"],
        ],
        resize_keyboard=True,
    )


def get_start_webapp_keyboard() -> InlineKeyboardMarkup:
    """Инлайн-кнопка для быстрого запуска WebApp из приветственного сообщения"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎬 Открыть Кино-Тиндер (Web App)",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )


def get_rec_card_keyboard(
    movie_id: int,
    current_genre: Optional[str] = None,
    user_reaction: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура под карточкой рекомендации (Tinder-style) с учетом реакции пользователя"""
    genre_btn_text = (
        f"🎭 Жанр: {current_genre.capitalize()}"
        if current_genre
        else "🎭 Выбрать жанр"
    )

    like_label = "❤️ Нравится ✅" if user_reaction == "LIKE" else "❤️ Нравится"
    dislike_label = "👎 Не моё ✅" if user_reaction == "DISLIKE" else "👎 Не моё"
    watch_label = "⏳ Буду смотреть ✅" if user_reaction == "WATCHLIST" else "⏳ Буду смотреть"

    buttons = [
        [
            InlineKeyboardButton(
                "📱 Свайпать в приложении",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ],
        [
            InlineKeyboardButton(like_label, callback_data=f"feed_like_{movie_id}"),
            InlineKeyboardButton(dislike_label, callback_data=f"feed_dislike_{movie_id}"),
        ],
        [
            InlineKeyboardButton(watch_label, callback_data=f"feed_watch_{movie_id}"),
            InlineKeyboardButton("➡️ Дальше", callback_data=f"feed_skip_{movie_id}"),
        ],
        [
            InlineKeyboardButton(genre_btn_text, callback_data="menu_filter_genre"),
            InlineKeyboardButton("🗂️ Списки", callback_data="menu_lists"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def get_blitz_keyboard(
    movie_id: int, current_index: int, total_count: int
) -> InlineKeyboardMarkup:
    """Клавиатура блиц-калибровки вкусов"""
    buttons = [
        [
            InlineKeyboardButton(
                "❤️ Понравилось",
                callback_data=f"blitz_like_{movie_id}_{current_index}",
            ),
            InlineKeyboardButton(
                "👎 Не понравилось",
                callback_data=f"blitz_dislike_{movie_id}_{current_index}",
            ),
        ],
        [
            InlineKeyboardButton(
                "⏩ Не смотрел / Пропустить",
                callback_data=f"blitz_skip_{movie_id}_{current_index}",
            ),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def get_search_card_keyboard(
    movie_id: int,
    user_reaction: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Клавиатура для карточки найденного фильма с учетом текущей реакции"""
    like_label = "❤️ В любимых ✅" if user_reaction == "LIKE" else "❤️ В любимые"
    watch_label = "⏳ В списке ✅" if user_reaction == "WATCHLIST" else "⏳ Буду смотреть"

    buttons = [
        [
            InlineKeyboardButton(like_label, callback_data=f"search_like_{movie_id}"),
            InlineKeyboardButton(watch_label, callback_data=f"search_watch_{movie_id}"),
        ],
        [
            InlineKeyboardButton("🎬 К рекомендациям", callback_data="feed_start"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def get_genre_filter_keyboard(
    active_genre: Optional[str] = None,
    active_type: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Клавиатура выбора типа контента и жанра для фильтрации рекомендаций"""
    buttons = [
        [
            InlineKeyboardButton(
                "🎬 Фильмы" + (" ✅" if active_type == "FILM" else ""),
                callback_data="set_type_FILM",
            ),
            InlineKeyboardButton(
                "📺 Сериалы" + (" ✅" if active_type == "TV_SERIES" else ""),
                callback_data="set_type_TV_SERIES",
            ),
            InlineKeyboardButton(
                "🌟 Любой" + (" ✅" if not active_type else ""),
                callback_data="reset_type",
            ),
        ]
    ]
    row = []
    for g in POPULAR_GENRES:
        title = f"✅ {g.capitalize()}" if active_genre == g else g.capitalize()
        row.append(InlineKeyboardButton(title, callback_data=f"set_genre_{g}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Кнопки сброса и возврата
    buttons.append(
        [
            InlineKeyboardButton("❌ Сбросить всё", callback_data="reset_genre"),
            InlineKeyboardButton("🎬 К рекомендациям", callback_data="feed_start"),
        ]
    )
    return InlineKeyboardMarkup(buttons)


def get_type_filter_keyboard(active_type: Optional[str] = None) -> InlineKeyboardMarkup:
    """Клавиатура выбора типа контента (фильмы / сериалы)"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎬 Фильмы" + (" ✅" if active_type == "FILM" else ""),
                    callback_data="set_type_FILM",
                ),
                InlineKeyboardButton(
                    "📺 Сериалы" + (" ✅" if active_type == "TV_SERIES" else ""),
                    callback_data="set_type_TV_SERIES",
                ),
            ],
            [
                InlineKeyboardButton(
                    "🌟 Любой контент" + (" ✅" if not active_type else ""),
                    callback_data="reset_type",
                ),
            ],
            [
                InlineKeyboardButton("🎬 К рекомендациям", callback_data="feed_start"),
            ],
        ]
    )


def get_lists_menu_keyboard(
    watchlist_count: int = 0, liked_count: int = 0
) -> InlineKeyboardMarkup:
    """Меню списков пользователя"""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"⏳ Буду смотреть ({watchlist_count})",
                    callback_data="list_view_WATCHLIST_0",
                ),
            ],
            [
                InlineKeyboardButton(
                    f"❤️ Понравившиеся ({liked_count})",
                    callback_data="list_view_LIKE_0",
                ),
            ],
            [
                InlineKeyboardButton("🎬 К рекомендациям", callback_data="feed_start"),
            ],
        ]
    )


def get_list_item_keyboard(
    movie_id: int, action: str, current_idx: int, total_count: int
) -> InlineKeyboardMarkup:
    """Клавиатура навигации по списку фильмов"""
    nav_row = []
    if current_idx > 0:
        nav_row.append(
            InlineKeyboardButton(
                "⬅️ Назад", callback_data=f"list_nav_{action}_{current_idx - 1}"
            )
        )
    nav_row.append(
        InlineKeyboardButton(
            f"{current_idx + 1}/{total_count}", callback_data="list_page_info"
        )
    )
    if current_idx < total_count - 1:
        nav_row.append(
            InlineKeyboardButton(
                "Вперед ➡️", callback_data=f"list_nav_{action}_{current_idx + 1}"
            )
        )

    action_row = []
    if action == "WATCHLIST":
        action_row.append(
            InlineKeyboardButton(
                "❤️ Посмотрел, понравилось", callback_data=f"list_like_{movie_id}"
            )
        )
        action_row.append(
            InlineKeyboardButton(
                "🗑️ Удалить", callback_data=f"list_del_{movie_id}_{current_idx}"
            )
        )

    menu_row = [
        InlineKeyboardButton("🗂️ Все списки", callback_data="menu_lists"),
        InlineKeyboardButton("🎬 Рекомендации", callback_data="feed_start"),
    ]

    rows = [nav_row]
    if action_row:
        rows.append(action_row)
    rows.append(menu_row)
    return InlineKeyboardMarkup(rows)

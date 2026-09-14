from enum import StrEnum

class FilmCollectionResponseItemsType(StrEnum):
    FILM = "FILM"
    MINI_SERIES = "MINI_SERIES"
    TV_SERIES = "TV_SERIES"
    TV_SHOW = "TV_SHOW"
    UNKNOWN = "UNKNOWN"
    VIDEO = "VIDEO"

    def __str__(self) -> str:
        return str(self.value)

from enum import StrEnum

class GetApiV22FilmsType(StrEnum):
    ALL = "ALL"
    FILM = "FILM"
    MINI_SERIES = "MINI_SERIES"
    TV_SERIES = "TV_SERIES"
    TV_SHOW = "TV_SHOW"

    def __str__(self) -> str:
        return str(self.value)

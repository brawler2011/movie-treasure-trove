from enum import StrEnum

class GetApiV22FilmsOrder(StrEnum):
    NUM_VOTE = "NUM_VOTE"
    RATING = "RATING"
    YEAR = "YEAR"

    def __str__(self) -> str:
        return str(self.value)

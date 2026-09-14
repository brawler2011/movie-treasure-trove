from enum import StrEnum

class ReviewResponseItemsType(StrEnum):
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)

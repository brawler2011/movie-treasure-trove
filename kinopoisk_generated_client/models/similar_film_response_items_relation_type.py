from enum import StrEnum

class SimilarFilmResponseItemsRelationType(StrEnum):
    SIMILAR = "SIMILAR"

    def __str__(self) -> str:
        return str(self.value)

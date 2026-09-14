from enum import StrEnum

class FilmSequelsAndPrequelsResponseRelationType(StrEnum):
    PREQUEL = "PREQUEL"
    REMAKE = "REMAKE"
    SEQUEL = "SEQUEL"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)

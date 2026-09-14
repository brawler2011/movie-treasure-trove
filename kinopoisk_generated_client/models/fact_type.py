from enum import StrEnum

class FactType(StrEnum):
    BLOOPER = "BLOOPER"
    FACT = "FACT"

    def __str__(self) -> str:
        return str(self.value)

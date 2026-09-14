from enum import StrEnum

class DistributionSubType(StrEnum):
    BLURAY = "BLURAY"
    CINEMA = "CINEMA"
    DIGITAL = "DIGITAL"
    DVD = "DVD"

    def __str__(self) -> str:
        return str(self.value)

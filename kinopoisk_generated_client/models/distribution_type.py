from enum import StrEnum

class DistributionType(StrEnum):
    ALL = "ALL"
    COUNTRY_SPECIFIC = "COUNTRY_SPECIFIC"
    LOCAL = "LOCAL"
    PREMIERE = "PREMIERE"
    WORLD_PREMIER = "WORLD_PREMIER"

    def __str__(self) -> str:
        return str(self.value)

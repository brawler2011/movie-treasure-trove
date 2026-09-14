from enum import StrEnum

class GetApiV22FilmsPremieresMonth(StrEnum):
    APRIL = "APRIL"
    AUGUST = "AUGUST"
    DECEMBER = "DECEMBER"
    FEBRUARY = "FEBRUARY"
    JANUARY = "JANUARY"
    JULY = "JULY"
    JUNE = "JUNE"
    MARCH = "MARCH"
    MAY = "MAY"
    NOVEMBER = "NOVEMBER"
    OCTOBER = "OCTOBER"
    SEPTEMBER = "SEPTEMBER"

    def __str__(self) -> str:
        return str(self.value)

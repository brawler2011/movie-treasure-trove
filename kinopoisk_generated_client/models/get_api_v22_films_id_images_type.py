from enum import StrEnum

class GetApiV22FilmsIdImagesType(StrEnum):
    CONCEPT = "CONCEPT"
    COVER = "COVER"
    FAN_ART = "FAN_ART"
    POSTER = "POSTER"
    PROMO = "PROMO"
    SCREENSHOT = "SCREENSHOT"
    SHOOTING = "SHOOTING"
    STILL = "STILL"
    UNKNOWN = "UNKNOWN"
    WALLPAPER = "WALLPAPER"

    def __str__(self) -> str:
        return str(self.value)

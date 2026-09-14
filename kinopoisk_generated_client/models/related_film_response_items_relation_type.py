from enum import StrEnum

class RelatedFilmResponseItemsRelationType(StrEnum):
    ALTERNATE_LANGUAGE = "ALTERNATE_LANGUAGE"
    EDITED_FROM = "EDITED_FROM"
    EDITED_INTO = "EDITED_INTO"
    PREQUEL = "PREQUEL"
    REFERENCES = "REFERENCES"
    REFERENCES_IN = "REFERENCES_IN"
    REMAKE = "REMAKE"
    SEQUEL = "SEQUEL"
    SIMILAR = "SIMILAR"
    SPIN_OFF = "SPIN_OFF"
    SPOOFED = "SPOOFED"
    SPOOFS = "SPOOFS"
    SPUN_OFF_FROM = "SPUN_OFF_FROM"
    VERSION = "VERSION"

    def __str__(self) -> str:
        return str(self.value)

from enum import StrEnum

class ApiKeyResponseAccountType(StrEnum):
    EXTENDED = "EXTENDED"
    FREE = "FREE"
    UNLIMITED = "UNLIMITED"

    def __str__(self) -> str:
        return str(self.value)

from enum import StrEnum

class PersonByNameResponseItemsSex(StrEnum):
    FEMALE = "FEMALE"
    MALE = "MALE"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)

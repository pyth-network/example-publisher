from enum import Enum


class SwapMode(str, Enum):
    EXACTIN = "ExactIn"
    EXACTOUT = "ExactOut"

    def __str__(self) -> str:
        return str(self.value)

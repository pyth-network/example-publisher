from enum import Enum


class GetQuoteSwapMode(str, Enum):
    EXACTIN = "ExactIn"
    EXACTOUT = "ExactOut"

    def __str__(self) -> str:
        return str(self.value)

from dataclasses import dataclass
from typing import List, Optional, Protocol

Symbol = str


@dataclass
class Price:
    price: float
    conf: float


class Provider(Protocol):
    def upd_products(self, product_symbols: List[Symbol]):
        ...

    def start(self):
        ...

    def latestPrice(self, symbol: Symbol) -> Optional[Price]:
        ...

from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from typing import List, Optional

Symbol = str


@dataclass
class Price:
    price: float
    conf: float


class Provider(ABC):
    @abstractmethod
    def upd_products(self, product_symbols: List[Symbol]):
        ...

    def start(self) -> None:
        asyncio.create_task(self._update_loop())

    @abstractmethod
    async def _update_loop(self):
        ...

    @abstractmethod
    def latest_price(self, symbol: Symbol) -> Optional[Price]:
        ...

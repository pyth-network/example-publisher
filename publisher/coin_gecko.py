import asyncio
from collections import defaultdict
from typing import DefaultDict
from pycoingecko import CoinGeckoAPI
from structlog import get_logger

log = get_logger()

Id = str
Price = float

USD = 'usd'


class CoinGecko:

    def __init__(self, update_interval_secs: int) -> None:
        self._api: CoinGeckoAPI = CoinGeckoAPI()
        self._prices: DefaultDict[Id, Price] = defaultdict(Price)
        self._update_interval_secs = update_interval_secs


    def start(self):
        asyncio.create_task(self._update_loop())


    def add_symbol(self, id_: Id) -> None:
        self._prices[id_] = 0


    async def _update_loop(self) -> None:
        while True:
            self._update_prices()
            await asyncio.sleep(self._update_interval_secs)


    def _update_prices(self) -> None:
        result = self._api.get_price(ids=list(self._prices.keys()), vs_currencies=USD)
        for id_, prices in result.items():
            self._prices[id_] = prices[USD]
        log.debug("updated prices from CoinGecko", prices=self._prices)


    def get_price(self, id_: Id) -> Price:
        return self._prices[id_]

import asyncio
from typing import List, Optional
from pythclient.hermes import HermesClient

from structlog import get_logger

from example_publisher.provider import Price, Provider, Symbol

from ..config import HermesConfig

log = get_logger()


class Hermes(Provider):
    def __init__(self, config: HermesConfig) -> None:
        self._config = config
        self._client = HermesClient([], config.http_endpoint, config.ws_endpoint)
        asyncio.run(self._get_hermes_prices())

    def upd_products(self, product_symbols: List[Symbol]) -> None:
        # TODO Optimize: Remove if possible any symbols we don't want any more
        self._client.add_feed_ids(product_symbols)
        pass

    def latest_price(self, symbol: Symbol) -> Optional[Price]:
        item = self._client.prices_dict[symbol]
        return Price(
            price=item.price.price,
            conf=item.price.conf,
            timestamp=item.price.publish_time
        )

    async def _get_hermes_prices(self):
        print("Starting web socket...")
        ws_call = self._client.ws_pyth_prices(version=1)
        ws_task = asyncio.create_task(ws_call)

        while True:
            await asyncio.sleep(5)
            if ws_task.done():
                break
            print("Latest prices:")
            for symbol, price_feed in self._client.prices_dict.items():
                print(f"Symbol: {symbol},"
                      f" Price: {price_feed['price'].price},"
                      f" Confidence: {price_feed['price'].conf},"
                      f" Time: {price_feed['price'].publish_time}")

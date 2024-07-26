import asyncio
from typing import List, Optional
from pythclient.hermes import HermesClient
# from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus


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
        # feed_ids = await self._client.get_price_feed_ids()
        # feed_ids_rel = feed_ids[:2]

        # self._client.add_feed_ids(feed_ids_rel)

        # prices_latest = await self._client.get_all_prices(version=version_http)

        # print("Initial prices")
        # for feed_id, price_feed in prices_latest.items():
        # print(f"Feed ID: {feed_id}, Price: {price_feed['price'].price}, Confidence: {price_feed['price'].conf}, Time: {price_feed['price'].publish_time}")

        print("Starting web socket...")
        ws_call = self._client.ws_pyth_prices(version=1)
        ws_task = asyncio.create_task(ws_call)

        while True:
            await asyncio.sleep(5)
            if ws_task.done():
                break
            # print("Latest prices:")
            # for feed_id, price_feed in self._client.prices_dict.items():
            #     print(f"Feed ID: {feed_id}, Price: {price_feed['price'].price}, Confidence: {price_feed['price'].conf}, Time: {price_feed['price'].publish_time}")

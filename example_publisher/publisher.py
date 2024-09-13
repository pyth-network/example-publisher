import asyncio
import time
from typing import Dict, List, Optional
from attr import define
from structlog import get_logger
from example_publisher.provider import Provider
from example_publisher.providers.coin_gecko import CoinGecko
from example_publisher.config import Config
from example_publisher.providers.pyth_replicator import PythReplicator
from example_publisher.pythd import PriceUpdate, Pythd, SubscriptionId


log = get_logger()

TRADING = "trading"


@define
class Product:
    generic_symbol: str
    symbol: str
    product_account: str
    price_account: str
    exponent: int
    subscription_id: Optional[SubscriptionId]


class Publisher:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self._product_update_task: asyncio.Task | None = None

        if not getattr(self.config, self.config.provider_engine):
            raise ValueError(f"Missing {self.config.provider_engine} config")

        if (
            self.config.provider_engine == "coin_gecko"
            and config.coin_gecko is not None
        ):
            self.provider = CoinGecko(config.coin_gecko)
        elif (
            self.config.provider_engine == "pyth_replicator"
            and config.pyth_replicator is not None
        ):
            self.provider: Provider = PythReplicator(config.pyth_replicator)
        else:
            raise ValueError(
                f"Unknown provider {self.config.provider_engine}, possibly the env variables are not set."
            )

        self.pythd: Pythd = Pythd(
            address=config.pythd.endpoint,
        )
        self.subscriptions: Dict[SubscriptionId, Product] = {}
        self.products: List[Product] = []
        self.last_successful_update: Optional[float] = None

    def is_healthy(self) -> bool:
        return (
            self.last_successful_update is not None
            and time.time() - self.last_successful_update
            < self.config.health_check_threshold_secs
        )

    async def start(self):
        await self.pythd.connect()

        self._product_update_task = asyncio.create_task(self._product_update_loop())

        self._price_update_task = asyncio.create_task(self._price_update_loop())

        await self._upd_products()
        self.provider.start()

    async def _product_update_loop(self):
        while True:
            await asyncio.sleep(self.config.product_update_interval_secs)
            await self._upd_products()

    async def _upd_products(self):
        log.debug("fetching product accounts from Pythd")
        pythd_products = {
            product.metadata.generic_symbol: product
            for product in await self.pythd.all_products()
        }
        log.debug("fetched product accounts from Pythd", products=pythd_products)

        old_products_by_generic_symbol = {
            product.generic_symbol: product for product in self.products
        }

        self.products = []

        for generic_symbol, product in pythd_products.items():
            if not product.prices:
                continue

            subscription_id = None
            if old_product := old_products_by_generic_symbol.get(generic_symbol):
                subscription_id = old_product.subscription_id

            self.products.append(
                Product(
                    generic_symbol,
                    product.metadata.symbol,
                    product.account,
                    product.prices[0].account,
                    product.prices[0].exponent,
                    subscription_id,
                )
            )

        self.provider.upd_products([product.symbol for product in self.products])

    async def _price_update_loop(self):
        while True:
            price_updates = []
            for product in self.products:
                price = self.provider.latest_price(product.symbol)
                if not price:
                    log.info("latest price not available", symbol=product.symbol)
                    continue

                scaled_price = self.apply_exponent(price.price, product.exponent)
                scaled_conf = self.apply_exponent(price.conf, product.exponent)

                price_updates.append(
                    PriceUpdate(
                        account=product.price_account,
                        price=scaled_price,
                        conf=scaled_conf,
                        status=TRADING,
                    )
                )

                self.last_successful_update = (
                    price.timestamp
                    if self.last_successful_update is None
                    else max(self.last_successful_update, price.timestamp)
                )

            log.info(
                "sending batch update_price",
                num_price_updates=len(price_updates),
            )

            await self.pythd.update_price_batch(price_updates)

            await asyncio.sleep(self.config.price_update_interval_secs)

    def apply_exponent(self, x: float, exp: int) -> int:
        return int(x * (10 ** (-exp)))

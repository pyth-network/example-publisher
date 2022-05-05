from typing import Any, Dict, List, Tuple
from attr import define
from structlog import get_logger
from publisher.aust import AUST

from publisher.coin_gecko import CoinGecko, Id as CoinGeckoId
from publisher.config import Config
from publisher.pythd import Pythd, Subscription
from random import randint


log = get_logger()

TRADING = 'trading'


class CoinGeckoPriceProvider:

  def __init__(self,
    coin_gecko: CoinGecko,
    coin_gecko_id: CoinGeckoId,
    confidence: int) -> None:
    self._coin_gecko = coin_gecko
    self._coin_gecko_id = coin_gecko_id
    self._confidence = confidence

  # Returns the latest price and confidence intervals, in USD
  def latestPrice(self) -> Tuple[int, int]:
    return self._coin_gecko.get_price(self._coin_gecko_id), self._confidence


class aUSTPriceProvider:

  def __init__(self, aust: AUST) -> None:
    self._aust = aust

  # Returns the latest price and confidence intervals, in UST
  def latestPrice(self) -> Tuple[int, int]:
    return self._aust.get_exchange_rate(), self._aust.get_confidence()


@define
class Product:
    symbol: str
    price_provider: Any
    product_account: str
    price_account: str
    exponent: int


class Publisher:

    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.coin_gecko: CoinGecko = CoinGecko(update_interval_secs=config.coin_gecko.update_interval_secs)
        self.aust = AUST(
          config.aust.terra_rpc_node,
          config.aust.chain_id,
          config.aust.anchor_money_market_contract_address,
          config.aust.update_interval_secs,
          config.aust.confidence_bps
        )
        self.pythd: Pythd = Pythd(address=config.pythd.endpoint, on_notify_price_sched=self.on_notify_price_sched)
        self.subscriptions: Dict[Subscription, Product] = {}
        self.products: List[Product] = []


    async def start(self):

      await self.pythd.connect()

      await self._initialize_products()

      await self._start_fetching_prices()

      await self._subscribe_notify_price_sched()


    async def _initialize_products(self):

        # Fetch all the product accounts from Pythd
        log.debug("fetching product accounts from Pythd")
        pythd_products = {
          product.metadata.symbol: product
          for product in await self.pythd.all_products()
        }
        log.debug("fetched product accounts from Pythd", products=pythd_products)

        # Create the products from the config
        for product in self.config.products:

          # Source AUST from the aUSTPriceProvider, use CoinGecko for everything else
          if product.pythd_symbol == self.config.aust.pythd_symbol:
            provider = aUSTPriceProvider(self.aust)
          else:
            provider = CoinGeckoPriceProvider(
                self.coin_gecko, product.coin_gecko_id, self.config.coin_gecko.confidence)

          self.products.append(
            Product(
              product.pythd_symbol,
              provider,
              pythd_products[product.pythd_symbol].account,
              pythd_products[product.pythd_symbol].prices[0].account,
              pythd_products[product.pythd_symbol].prices[0].exponent)
          )


    async def _start_fetching_prices(self):
        for product in self.config.products:
          self.coin_gecko.add_symbol(product.coin_gecko_id)
        self.coin_gecko.start()
        self.aust.start()


    async def _subscribe_notify_price_sched(self):
        # Subscribe to Pythd's notify_price_sched for each product
        log.debug("subscribing to notify_price_sched")
        self.subscriptions = {
          await self.pythd.subscribe_price_sched(product.price_account): product
          for product in self.products
        }
        

    async def on_notify_price_sched(self, subscription: int) -> None:

      log.debug("received notify_price_sched", subscription=subscription)
      if subscription not in self.subscriptions:
        return

      # Look up the current price and confidence interval of the product
      product = self.subscriptions[subscription]
      price, conf = product.price_provider.latestPrice()
      if price is None or conf is None:
        log.warn("latest price not available", symbol=product.symbol)
        return 

      # Scale the price and confidence interval using the Pyth exponent 
      scaled_price = self.apply_exponent(price, product.exponent)
      scaled_conf = self.apply_exponent(conf, product.exponent)

      # Send the price update
      log.debug("sending update_price",
        product_account=product.product_account,
        price_account=product.price_account,
        price=scaled_price,
        conf=scaled_conf)
      await self.pythd.update_price(
        product.price_account,
        scaled_price,
        scaled_conf,
        TRADING)

    def apply_exponent(self, x: float, exp: int) -> int:
      return int(x * (10 ** (-exp)))

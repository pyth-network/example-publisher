from typing import Any, Dict, List, Protocol, Tuple
from attr import define
from structlog import get_logger

from publisher.coin_gecko import CoinGecko, Id as CoinGeckoId
from publisher.config import Config
from publisher.pythd import Pythd, Subscription
from random import randint


log = get_logger()

TRADING = 'trading'

class Provider(Protocol):
  def latestPrice(self) -> Tuple[float, float]:
     ...


class CoinGeckoPriceProvider(Provider):

  def __init__(self,
    coin_gecko: CoinGecko,
    coin_gecko_id: CoinGeckoId,
    confidence_ratio_bps: int) -> None:
    self._coin_gecko = coin_gecko
    self._coin_gecko_id = coin_gecko_id
    self._confidence_ratio_bps = confidence_ratio_bps

  # Returns the latest price and confidence intervals, in USD
  def latestPrice(self) -> Tuple[float, float]:
    price = self._coin_gecko.get_price(self._coin_gecko_id)
    return price, price * self._confidence_ratio_bps / 10000

@define
class Product:
    symbol: str
    price_provider: Provider
    product_account: str
    price_account: str
    exponent: int


class Publisher:

    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.coin_gecko: CoinGecko = CoinGecko(
           update_interval_secs=config.coin_gecko.update_interval_secs
        ) if config.coin_gecko else None

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

          if self.coin_gecko:
            provider = CoinGeckoPriceProvider(
                self.coin_gecko, product.coin_gecko_id, self.config.coin_gecko.confidence_ratio_bps)
          else:
             raise ValueError(f"Symbol {product.pythd_symbol} has no provider.")

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
        
        if self.coin_gecko:
          self.coin_gecko.start()

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
        conf=scaled_conf,
        symbol=product.symbol)
      await self.pythd.update_price(
        product.price_account,
        scaled_price,
        scaled_conf,
        TRADING)

    def apply_exponent(self, x: float, exp: int) -> int:
      return int(x * (10 ** (-exp)))

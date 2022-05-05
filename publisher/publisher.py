from typing import Dict, List
from attr import define
import numpy as np
from structlog import get_logger

from publisher.coin_gecko import CoinGecko
from publisher.config import Config
from publisher.pythd import Pythd, Subscription
from random import randint


log = get_logger()

TRADING = 'trading'


@define
class Product:
    symbol: str
    coin_gecko_id: str
    product_account: str
    price_account: str
    exponent: int


class Publisher:

    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.coin_gecko: CoinGecko = CoinGecko(update_interval_secs=config.coin_gecko.update_interval_secs)
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

        # Associate the symbol with the CoinGecko ID and Pythd price account
        self.products = [
          Product(
            product.pythd_symbol, 
            product.coin_gecko_id,
            pythd_products[product.pythd_symbol].account,
            pythd_products[product.pythd_symbol].prices[0].account,
            pythd_products[product.pythd_symbol].prices[0].exponent)
          for product in self.config.products
        ]
        log.debug("associated product symbols", products=self.products)


    async def _start_fetching_prices(self):
        for product in self.config.products:
          self.coin_gecko.add_symbol(product.coin_gecko_id)
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

      # Look up the current price of the product from CoinGecko, apply fuzz and scaling
      product = self.subscriptions[subscription]
      coin_gecko_price = self.coin_gecko.get_price(product.coin_gecko_id)
      if not coin_gecko_price:
        log.warn("CoinGecko price not available", symbol=product.symbol, coin_gecko_id=product.coin_gecko_id)
        return 

      price = self.apply_exponent(
          self.coin_gecko.get_price(product.coin_gecko_id), product.exponent)

      # Hard-code the confidence interval
      conf = self.apply_exponent(self.config.pythd.confidence, product.exponent)
      
      log.debug("sending update_price", product_account=product.product_account, price_account=product.price_account, price=price, conf=conf)
      await self.pythd.update_price(product.price_account, price, conf, TRADING)

    def apply_exponent(self, x: float, exp: int) -> int:
      return int(x * (10 ** (-exp)))

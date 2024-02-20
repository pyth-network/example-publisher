import asyncio
import requests
from typing import Dict, List, Optional
from structlog import get_logger

from example_publisher.provider import Price, Provider, Symbol
from ..config import RoninKatanaConfig

log = get_logger()

Id = str  # The "API id" of the CoinGecko price, listed on CoinGecko page for each coin.


class RoninKatana(Provider):
    def __init__(self, config: RoninKatanaConfig) -> None:
        self._prices: Dict[Id, float] = {}
        self._symbol_to_id: Dict[Symbol, Id] = {
            product.symbol: product.id for product in config.products
        }
        self._config = config

    def generate_header(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authority": "api.roninchain.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
        }

    def upd_products(self, product_symbols: List[Symbol]) -> None:
        new_prices = {}
        for ronin_katana_product in self._config.products:
            if ronin_katana_product.symbol in product_symbols:
                new_prices[ronin_katana_product.id] = self._prices.get(ronin_katana_product.id, None)
            else:
                raise ValueError(
                    f"{ronin_katana_product.symbol} not found in available products"  # noqa: E713
                )
        self._prices = new_prices

    async def _update_loop(self) -> None:
        while True:
            self._update_prices()
            await asyncio.sleep(self._config.update_interval_secs)

    def _get_price_from_katana(self, ids: List[str]) -> Dict[Id, float]:
        """
            currentPrice = parseFloat(wronTokenData.derivedETH) * ethExchangeInfo.currentPrice
        """
        # Get current price

        result = {token_id: 0 for token_id in ids}
        resp = requests.post(
            url=f"{self._config.https_analytic_endpoint}/subgraphs/name/axieinfinity/katana-subgraph-blue",
            headers=self.generate_header(),
            json={
                "query": "query bundles {\n  bundles(where: {id: 1}) {\n    id\n    ethPrice\n    __typename\n  }\n}\n",
                "variables": {}})

        response = resp.json()
        eth_price = response["data"]["bundles"][0]["ethPrice"]
        # Get ronin volume
        resp = requests.post(
            url=f"{self._config.https_analytic_endpoint}/subgraphs/name/axieinfinity/katana-subgraph-blue",
            headers=self.generate_header(),
            json={
                "operationName": "tokens", "variables": {},
                "query": "fragment TokenFields on Token {\n  id\n  name\n  symbol\n  derivedETH\n  tradeVolume\n  tradeVolumeUSD\n  untrackedVolumeUSD\n  totalLiquidity\n  txCount\n  __typename\n}\n\nquery tokens {\n  tokens(first: 200, orderBy: tradeVolumeUSD, orderDirection: desc) {\n    ...TokenFields\n    __typename\n  }\n}\n"})

        response = resp.json()
        tokens = response["data"]["tokens"]
        for token in tokens:
            if token["symbol"] in result.keys():
                result[token["symbol"]] = float(eth_price) * float(token["derivedETH"])

        for k in list(result.keys()):
            if result[k] == 0:
                del result[k]
        log.info("Get price from Katana", result=result)
        return result

    # Logic here we need to get price from Katana and update it into dict _prices
    def _update_prices(self) -> None:
        # We need to implement logic here
        result = self._get_price_from_katana(ids=list(self._prices.keys()))
        for id_, price in result.items():
            self._prices[id_] = price
        log.info("updated prices from Katana", prices=self._prices)

    def _get_price(self, id: Id) -> float:
        return self._prices.get(id, None)

    # Crypto.BTC/USD in our case.
    def latest_price(self, symbol: Symbol) -> Optional[Price]:
        id = self._symbol_to_id.get(symbol)
        if not id:
            return None

        price = self._get_price(id)
        if not price:
            return None
        return Price(price, price * self._config.confidence_ratio_bps / 10000)
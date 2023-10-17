import asyncio
from http import HTTPStatus
from typing import Dict, List, Optional
from structlog import get_logger

from example_publisher.provider import Price, Provider, Symbol
from ..config import JupiterConfig, JupiterProduct
from jupiter_api_v_6_client import Client
from jupiter_api_v_6_client.api.default import get_quote
from jupiter_api_v_6_client.models import QuoteResponse
from jupiter_api_v_6_client.types import Response

log = get_logger()

Id = str  # The "API id" of the price, the mint

# 1 USD is 1 USDC
USD = "usd"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
USDC_DECIMALS = 6
USDC_AMOUNT = 100_000_000 # ~100 USD

async def get_price(client: Client, input_mint: str, output_mint: str, amount: int, input_decimals, output_decimals, is_input_quote: bool) -> Optional[float]:
    response: Response[QuoteResponse] = await get_quote.asyncio_detailed(
        client=client,
        input_mint=input_mint,
        output_mint=output_mint,
        amount=amount
    )
    if response.status_code == HTTPStatus.OK:
        out_amount = int(response.parsed.out_amount)
        if is_input_quote:
            return out_amount / amount * 10**(input_decimals - output_decimals)
        else:
            return amount / out_amount * 10**(output_decimals - input_decimals)
    return None

async def compute_price_from_jupiter(client: Client, product: JupiterProduct) -> Optional[Price]:
    """Only supports ticker/USD for now
    Compute buy/sell spread and use it as confidence,
    gas is negligeable in our case assuming 0 congestion 
    To price the asset we take $10 of value and swap back and forth"""
    print('before get_price')
    buy_price = await get_price(client, product.mint, USDC, USDC_AMOUNT, product.decimals, USDC_DECIMALS, is_input_quote=True)
    print('buy_price', buy_price)
    if not buy_price:
        return None
    sell_amount = int(USDC_AMOUNT / buy_price * 10**(product.decimals - USDC_DECIMALS))
    print('sell_amount', sell_amount)
    sell_price = await get_price(client, USDC, product.mint, sell_amount, USDC_DECIMALS, product.decimals, is_input_quote=False)
    print('sell_price', sell_price)
    if not sell_price:
        return None

    mid_price = (sell_price + buy_price) / 2
    spread = abs(sell_price - buy_price) / 2

    return Price(mid_price, conf=spread)

class Jupiter(Provider):
    def __init__(self, config: JupiterConfig) -> None:
        self._api_client: Client = Client(base_url=config.base_url)
        self._prices: Dict[Id, Price | None] = {}
        self._symbol_to_id: Dict[Symbol, Id] = {
            product.symbol: product.mint for product in config.products
        }
        self._config = config

    def upd_products(self, product_symbols: List[Symbol]) -> None:
        new_prices = {}
        filtered_product_symbols = []
        for product in self._config.products:
            if product.symbol in product_symbols:
                mint = product.mint
                new_prices[mint] = self._prices.get(mint, None)
                filtered_product_symbols.append(product.symbol)
            else:
                raise ValueError(
                    f"{product.symbol} not found in available products"
                )

        self._prices = new_prices
        return filtered_product_symbols

    async def _update_loop(self) -> None:
        while True:
            await self._update_prices()
            await asyncio.sleep(self._config.update_interval_secs)

    async def _update_prices(self) -> None:
        for product in self._config.products:
            price = await compute_price_from_jupiter(self._api_client, product)
            self._prices[product.mint] = price
        log.info("updated prices from Jupiter", prices=self._prices)

    def latest_price(self, symbol: Symbol) -> Optional[Price]:
        id = self._symbol_to_id.get(symbol)
        if not id:
            return None
        price = self._prices.get(id, None)
        return price

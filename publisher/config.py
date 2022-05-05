from typing import List
import typed_settings as ts

@ts.settings
class Product:
    # The value of attr_dict["symbol"] for this product, which will be used to retrieve the price account
    pythd_symbol: str
    # The CoinGecko API ID for this product, used to query reference prices
    coin_gecko_id: str


@ts.settings
class Pythd:
    # The websocket endpoint
    endpoint: str


@ts.settings
class CoinGecko:
    # How often to poll CoinGecko for price information
    update_interval_secs: int
    # The confidence interval to use for CoinGecko updates
    confidence: int

@ts.settings
class Config:
    pythd: Pythd
    coin_gecko: CoinGecko
    products: List[Product]

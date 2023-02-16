from typing import List, Optional
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
    # The confidence interval rate (to the price) in basis points to use for CoinGecko updates
    confidence_ratio_bps: int


@ts.settings
class AUST:
    # The Terra RPC node to use to query contracts
    terra_rpc_node: str
    # The Chain ID to connect to
    chain_id: str
    # The address of the Anchor Money Market contract to query the AUST exchange rate from
    anchor_money_market_contract_address: str
    # How often to query the exchange rate from the Anchor Money Market contract
    update_interval_secs: int
    # The Pythd symbol
    pythd_symbol: str
    # The confidence interval in basis points
    confidence_bps: int


@ts.settings
class Config:
    pythd: Pythd
    products: List[Product]
    coin_gecko: Optional[CoinGecko] = ts.option(default=None)

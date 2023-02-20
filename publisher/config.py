from typing import List, Optional
import typed_settings as ts


@ts.settings
class CoinGeckoProduct:
    # Symbol name. e.g., Crypto.BTC/USD
    symbol: str
    # The CoinGecko API ID for this product, used to query reference prices
    coin_gecko_id: Optional[str] = ts.option(default=None)


@ts.settings
class Pythd:
    # The websocket endpoint
    endpoint: str


@ts.settings
class CoinGeckoConfig:
    # How often to poll CoinGecko for price information
    update_interval_secs: int
    # The confidence interval rate (to the price) in basis points to use for CoinGecko updates
    confidence_ratio_bps: int
    products: List[CoinGeckoProduct]


@ts.settings
class PythReplicatorConfig:
    http_endpoint: str
    ws_endpoint: str
    first_mapping: str
    program_key: str
    staleness_time_in_secs: int = ts.option(default=30)
    account_update_interval_secs: int = ts.option(default=300)


@ts.settings
class Config:
    provider_engine: str
    pythd: Pythd
    product_update_interval_secs: int = ts.option(default=60)
    coin_gecko: Optional[CoinGeckoConfig] = ts.option(default=None)
    pyth_replicator: Optional[PythReplicatorConfig] = ts.option(default=None)

from typing import List, Optional
import typed_settings as ts


@ts.settings
class CoinGeckoProduct:
    # Symbol name. e.g., Crypto.BTC/USD
    symbol: str
    # The CoinGecko API ID for this product, used to query reference prices
    coin_gecko_id: str


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
class JupiterProduct:
    # Symbol name. e.g., Crypto.BTC/USD
    symbol: str
    # The base58 mint
    mint: str
    decimals: int


@ts.settings
class JupiterConfig:
    base_url: str
    # How often to poll jupiter for price information
    update_interval_secs: int
    products: List[JupiterProduct]

@ts.settings
class PythReplicatorConfig:
    http_endpoint: str
    ws_endpoint: str
    first_mapping: str
    program_key: str
    staleness_time_in_secs: int = ts.option(default=30)
    # Manual aggregation is aggregating the prices of the publishers and ignoring
    # the min_publishers when aggregate price status is not TRADING. This will improve
    # the feed uptime but reduces the accuracy of the feed. One benefit of this feature
    # is mirroring coming soon feeds on the target network that have some beta publishers.
    manual_agg_enabled: bool = ts.option(default=True)
    # The maximum slot difference to consider a publisher for manual aggregation
    # when the aggregate price status is not TRADING.
    manual_agg_max_slot_diff: int = ts.option(default=25)
    account_update_interval_secs: int = ts.option(default=300)


@ts.settings
class Config:
    provider_engine: str
    pythd: Pythd
    product_update_interval_secs: int = ts.option(default=60)
    coin_gecko: Optional[CoinGeckoConfig] = ts.option(default=None)
    pyth_replicator: Optional[PythReplicatorConfig] = ts.option(default=None)

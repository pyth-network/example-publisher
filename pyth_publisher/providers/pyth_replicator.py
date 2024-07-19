import asyncio
from typing import Dict, List, Optional, Tuple
from pythclient.pythclient import PythClient
from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus
import time


from structlog import get_logger

from pyth_publisher.provider import Price, Provider, Symbol

from ..config import PythReplicatorConfig

log = get_logger()


# Any feed with >= this number of min publishers is considered "coming soon".
COMING_SOON_MIN_PUB_THRESHOLD = 10


class PythReplicator(Provider):
    def __init__(self, config: PythReplicatorConfig) -> None:
        self._config = config
        self._client = PythClient(
            solana_endpoint=config.http_endpoint,
            solana_ws_endpoint=config.ws_endpoint,
            first_mapping_account_key=config.first_mapping,
            program_key=config.program_key,
        )
        self._prices: Dict[str, Optional[Price]] = {}
        self._update_accounts_task: asyncio.Task | None = None

    async def _update_loop(self) -> None:
        self._ws = self._client.create_watch_session()
        log.info("Creating Pyth replicator WS")

        await self._ws.connect()
        await self._ws.program_subscribe(
            self._config.program_key, await self._client.get_all_accounts()
        )

        self._update_accounts_task = asyncio.create_task(self._update_accounts_loop())

        while True:
            update = await self._ws.next_update()
            log.debug("Received a WS update", account_key=update.key, slot=update.slot)
            if isinstance(update, PythPriceAccount) and update.product is not None:
                symbol = update.product.symbol

                if self._prices.get(symbol) is None:
                    self._prices[symbol] = None

                if (
                    update.aggregate_price_status == PythPriceStatus.TRADING
                    and update.aggregate_price is not None
                    and update.aggregate_price_confidence_interval is not None
                ):
                    self._prices[symbol] = Price(
                        update.aggregate_price,
                        update.aggregate_price_confidence_interval,
                        update.timestamp,
                    )
                elif (
                    self._config.manual_agg_enabled
                    and update.min_publishers is not None
                    and update.min_publishers >= COMING_SOON_MIN_PUB_THRESHOLD
                ):
                    # Do the manual aggregation based on the recent active publishers
                    # and their confidence intervals if possible. This will allow us to
                    # get an aggregate if there are some active publishers but they are
                    # not enough to reach the min_publishers threshold.
                    #
                    # Note that we only manually aggregate for feeds that are coming soon. Some feeds should go
                    # offline outside of market hours (e.g., Equities, Metals). Manually aggregating for these feeds
                    # can cause them to come online at unexpected times if a single data provider publishes at that time.
                    prices: List[float] = []

                    current_slot = update.slot
                    for price_component in update.price_components:
                        price = price_component.latest_price_info
                        if (
                            price.price_status == PythPriceStatus.TRADING
                            and current_slot is not None
                            and current_slot - price.pub_slot
                            <= self._config.manual_agg_max_slot_diff
                        ):
                            prices.extend(
                                [
                                    price.price - price.confidence_interval,
                                    price.price,
                                    price.price + price.confidence_interval,
                                ]
                            )
                            break

                    if prices:
                        agg_price, agg_confidence_interval = manual_aggregate(prices)

                        self._prices[symbol] = Price(
                            agg_price, agg_confidence_interval, update.timestamp
                        )

                log.info(
                    "Received a price update", symbol=symbol, price=self._prices[symbol]
                )

    async def _update_accounts_loop(self) -> None:
        while True:
            log.info("Update Pyth accounts")
            await self._client.refresh_products()
            await self._client.refresh_all_prices()
            self._ws.update_program_accounts(
                self._config.program_key, await self._client.get_all_accounts()
            )
            log.info("Finished updating Pyth accounts")

            await asyncio.sleep(self._config.account_update_interval_secs)

    def upd_products(self, *args) -> None:
        # This provider stores all the possible feeds and
        # does not care about the desired products as knowing
        # them does not improve the performance of the replicator
        # websocket. Although the websocket filters the given accounts
        # but this filtering happens in the client-side and not on the server-side.
        pass

    def latest_price(self, symbol: Symbol) -> Optional[Price]:
        price = self._prices.get(symbol, None)

        if not price:
            return None

        if time.time() - price.timestamp > self._config.staleness_time_in_secs:
            return None

        return price


def manual_aggregate(prices: List[float]) -> Tuple[float, float]:
    """
    This function is used to manually aggregate the prices of the active publishers. This is a very simple
    implementation that does not get the aggregate and confidence accurately but it is good enough for our use case.
    On this implementation, if the aggregate or confidence are not an element of the list, then we consider the
    rightmost element lower than them in the list. For example, if the list is [1, 2, 3, 4] instead of using
    median 2.5 as aggregate we use 2.
    """
    prices.sort()
    num_prices = len(prices)

    agg_price = prices[num_prices // 2]

    agg_confidence_interval_left = agg_price - prices[num_prices // 4]
    agg_confidence_interval_right = prices[num_prices * 3 // 4] - agg_price

    agg_confidence_interval = max(
        agg_confidence_interval_left, agg_confidence_interval_right
    )

    return agg_price, agg_confidence_interval

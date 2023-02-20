import asyncio
from typing import Dict, List, Optional, Tuple
from pythclient.pythclient import PythClient
from pythclient.pythaccounts import PythPriceAccount
import time


from structlog import get_logger

from publisher.provider import Price, Provider, Symbol

from ..config import PythReplicatorConfig

log = get_logger()

UnixTimestamp = int


class PythReplicator(Provider):
    def __init__(self, config: PythReplicatorConfig) -> None:
        self._config = config
        self._client = PythClient(
            solana_endpoint=config.http_endpoint,
            solana_ws_endpoint=config.ws_endpoint,
            first_mapping_account_key=config.first_mapping,
            program_key=config.program_key,
        )
        self._prices: Dict[
            str, Tuple[float | None, float | None, UnixTimestamp | None]
        ] = {}

    def start(self) -> None:
        asyncio.create_task(self._ws_loop())

    async def _ws_loop(self) -> None:
        self._ws = self._client.create_watch_session()
        log.info("Creating Pyth replicator WS")

        await self._ws.connect()
        await self._ws.program_subscribe(
            self._config.program_key, await self._client.get_all_accounts()
        )

        asyncio.create_task(self._update_accounts_loop())

        while True:
            update = await self._ws.next_update()
            log.debug("Received a WS update", account_key=update.key, slot=update.slot)
            if isinstance(update, PythPriceAccount):
                symbol = update.product.symbol

                self._prices[symbol] = [
                    update.aggregate_price,
                    update.aggregate_price_confidence_interval,
                    update.timestamp,
                ]

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

    def upd_products(self, _: List[Symbol]) -> None:
        # This provider stores all the possible feeds and
        # does not care about the desired products as knowing
        # them does not improve the performance of the replicator
        # websocket. Although the websocket filters the given accounts
        # but this filtering happens in the client-side and not on the server-side.
        pass

    def latest_price(self, symbol: Symbol) -> Optional[Price]:
        price, conf, timestamp = self._prices.get(symbol, [None, None, None])

        if not price or not conf or not timestamp:
            return None

        if time.time() - timestamp > self._config.staleness_time_in_secs:
            return None

        return Price(price, conf)

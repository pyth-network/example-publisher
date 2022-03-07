import asyncio
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import Awaitable, Callable, List
from structlog import get_logger
from jsonrpc_websocket import Server

log = get_logger()

Subscription = int
Status = str

TRADING = "trading"


@dataclass_json
@dataclass
class Price:
    account: str


@dataclass_json
@dataclass
class Metadata:
    symbol: str


@dataclass_json
@dataclass
class Product:
    account: str
    metadata: Metadata = field(metadata=config(field_name="attr_dict"))
    prices: List[Price] = field(metadata=config(field_name="price"))


class Pythd:

    def __init__(self, address: str, on_notify_price_sched: Callable[[Subscription], Awaitable]) -> None:
        self.address = address
        self.server: Server = None
        self.on_notify_price_sched = on_notify_price_sched


    async def connect(self) -> Server:
        self.server = Server(self.address)
        self.server.notify_price_sched = self._notify_price_sched
        await self.server.ws_connect()


    async def subscribe_price_sched(self, account: str) -> int:
        subscription = (await self.server.subscribe_price_sched(account=account))['subscription']
        log.debug("subscribed to price_sched", account=account, subscription=subscription)
        return subscription


    def _notify_price_sched(self, subscription: int) -> None:
        log.debug("notify_price_sched RPC call received", subscription=subscription)
        asyncio.get_event_loop().create_task(self.on_notify_price_sched(subscription))


    async def all_products(self) -> List[Product]:
        result = await self.server.get_product_list()
        return [Product.from_dict(d) for d in result]


    async def update_price(self, account: str, price: int, conf: int, status: str) -> None:
        await self.server.update_price(account=account, price=price, conf=conf, status=status)

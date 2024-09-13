from dataclasses import dataclass, field
from dataclasses_json import config, DataClassJsonMixin
from typing import List, Any, Optional
from structlog import get_logger
from websockets.client import connect, WebSocketClientProtocol
from asyncio import Lock

log = get_logger()

SubscriptionId = int
Status = str

TRADING = "trading"


@dataclass
class Price(DataClassJsonMixin):
    account: str
    exponent: int = field(metadata=config(field_name="price_exponent"))


@dataclass
class PriceUpdate(DataClassJsonMixin):
    account: str
    price: int
    conf: int
    status: str


@dataclass
class Metadata(DataClassJsonMixin):
    symbol: str
    generic_symbol: str


@dataclass
class Product(DataClassJsonMixin):
    account: str
    metadata: Metadata = field(metadata=config(field_name="attr_dict"))
    prices: List[Price] = field(metadata=config(field_name="price"))


@dataclass
class JSONRPCRequest(DataClassJsonMixin):
    id: int
    method: str
    params: List[Any] | Any
    jsonrpc: str = "2.0"


@dataclass
class JSONRPCResponse(DataClassJsonMixin):
    id: int
    result: Optional[Any]
    error: Optional[Any]
    jsonrpc: str = "2.0"


class Pythd:
    def __init__(
        self,
        address: str,
    ) -> None:
        self.address = address
        self.client: WebSocketClientProtocol
        self.id_counter = 0
        self.lock = Lock()

    async def connect(self):
        self.client = await connect(self.address)

    def _create_request(self, method: str, params: List[Any] | Any) -> JSONRPCRequest:
        self.id_counter += 1
        return JSONRPCRequest(
            id=self.id_counter,
            method=method,
            params=params,
        )

    async def send_request(self, request: JSONRPCRequest) -> JSONRPCResponse:
        async with self.lock:
            await self.client.send(request.to_json())
            response = await self.client.recv()
            return JSONRPCResponse.from_json(response)

    async def send_batch_request(
        self, requests: List[JSONRPCRequest]
    ) -> List[JSONRPCResponse]:
        async with self.lock:
            await self.client.send(JSONRPCRequest.schema().dumps(requests, many=True))
            response = await self.client.recv()
            return JSONRPCResponse.schema().loads(response, many=True)

    async def all_products(self) -> List[Product]:
        request = self._create_request("get_product_list", [])
        result = await self.send_request(request)
        if result.result:
            return Product.schema().load(result.result, many=True)
        else:
            raise ValueError(f"Error fetching products: {result.to_json()}")

    async def update_price_batch(self, price_updates: List[PriceUpdate]) -> None:
        requests = [
            self._create_request("update_price", price_update.to_dict())
            for price_update in price_updates
        ]
        results = await self.send_batch_request(requests)
        if any(result.error for result in results):
            results_json_str = JSONRPCResponse.schema().dumps(results, many=True)
            raise ValueError(f"Error updating prices: {results_json_str}")

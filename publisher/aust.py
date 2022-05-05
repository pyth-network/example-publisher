from typing import Tuple
from terra_sdk.client.lcd import AsyncLCDClient
from dataclasses_json import dataclass_json
from dataclasses import dataclass
import asyncio
from structlog import get_logger


log = get_logger()

@dataclass_json
@dataclass
class EpochState:
    exchange_rate: str

class AUST:

  def __init__(self,
    rpc_node: str,
    chain_id: str,
    contract_addr: str,
    update_interval_secs: int,
    confidence_bps: int) -> None:
    self._client = AsyncLCDClient(rpc_node, chain_id)
    self._update_interval_secs = update_interval_secs
    self._contract_addr = contract_addr
    self._confidence_bps = confidence_bps
    self._current_exchange_rate = None
    self._current_confidence = None


  def start(self):
    asyncio.create_task(self._update_loop())


  async def _update_loop(self) -> None:
    while True:
      await self._update_exchange_rate()

      await asyncio.sleep(self._update_interval_secs)


  async def _update_exchange_rate(self) -> None:
    epoch_state = EpochState.from_dict(
      await self._client.wasm.contract_query(self._contract_addr, {"epoch_state": {}})
    )
    self._current_exchange_rate = float(epoch_state.exchange_rate)
    self._current_confidence = self._current_exchange_rate * (self._confidence_bps / 10000)
    log.debug("updated exchange rate for AUST",
      exchange_rate=self._current_exchange_rate,
      confidence=self._current_confidence)


  def get_exchange_rate(self) -> float:
    return self._current_exchange_rate


  def get_confidence(self) -> float:
    return self._current_confidence

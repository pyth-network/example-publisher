import asyncio

from jupiter_api_v_6_client.client import Client
from ..config import JupiterConfig, JupiterProduct
from example_publisher.providers.jupiter import USDC, Jupiter, get_price
import pytest

BSOL_MINT = "bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1"

@pytest.mark.asyncio
async def test_get_price():
    client = Client(base_url="https://quote-api.jup.ag/v6")
    price = await get_price(client, input_mint=USDC, output_mint=BSOL_MINT, amount=100_000_000, input_decimals=6, output_decimals=9, is_input_quote=True)
    assert price

@pytest.mark.asyncio
async def test_jupiter_works():
    symbol = "Crypto.BSOL/USD"
    config = JupiterConfig(
        base_url="https://quote-api.jup.ag/v6",
        update_interval_secs=1, 
        products=[JupiterProduct(mint=BSOL_MINT, symbol=symbol, decimals=9)]
    )

    jupiter = Jupiter(config)
    jupiter.start()

    await asyncio.sleep(1)

    latest_price = jupiter.latest_price(symbol)
    print(f"latest_price: {latest_price}")


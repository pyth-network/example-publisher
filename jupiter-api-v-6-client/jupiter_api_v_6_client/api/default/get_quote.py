from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_quote_exclude_dexes_item import GetQuoteExcludeDexesItem
from ...models.get_quote_swap_mode import GetQuoteSwapMode
from ...models.quote_response import QuoteResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    input_mint: str,
    output_mint: str,
    amount: int,
    slippage_bps: Union[Unset, None, int] = UNSET,
    swap_mode: Union[Unset, None, GetQuoteSwapMode] = UNSET,
    exclude_dexes: Union[Unset, None, List[GetQuoteExcludeDexesItem]] = UNSET,
    only_direct_routes: Union[Unset, None, bool] = UNSET,
    as_legacy_transaction: Union[Unset, None, bool] = UNSET,
    platform_fee_bps: Union[Unset, None, int] = UNSET,
    max_accounts: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["inputMint"] = input_mint

    params["outputMint"] = output_mint

    params["amount"] = amount

    params["slippageBps"] = slippage_bps

    json_swap_mode: Union[Unset, None, str] = UNSET
    if not isinstance(swap_mode, Unset):
        json_swap_mode = swap_mode.value if swap_mode else None

    params["swapMode"] = json_swap_mode

    json_exclude_dexes: Union[Unset, None, List[str]] = UNSET
    if not isinstance(exclude_dexes, Unset):
        if exclude_dexes is None:
            json_exclude_dexes = None
        else:
            json_exclude_dexes = []
            for exclude_dexes_item_data in exclude_dexes:
                exclude_dexes_item = exclude_dexes_item_data.value

                json_exclude_dexes.append(exclude_dexes_item)

    params["excludeDexes"] = json_exclude_dexes

    params["onlyDirectRoutes"] = only_direct_routes

    params["asLegacyTransaction"] = as_legacy_transaction

    params["platformFeeBps"] = platform_fee_bps

    params["maxAccounts"] = max_accounts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/quote",
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[QuoteResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QuoteResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[QuoteResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    input_mint: str,
    output_mint: str,
    amount: int,
    slippage_bps: Union[Unset, None, int] = UNSET,
    swap_mode: Union[Unset, None, GetQuoteSwapMode] = UNSET,
    exclude_dexes: Union[Unset, None, List[GetQuoteExcludeDexesItem]] = UNSET,
    only_direct_routes: Union[Unset, None, bool] = UNSET,
    as_legacy_transaction: Union[Unset, None, bool] = UNSET,
    platform_fee_bps: Union[Unset, None, int] = UNSET,
    max_accounts: Union[Unset, None, int] = UNSET,
) -> Response[QuoteResponse]:
    """GET /quote

     Sends a GET request to the Jupiter API to get the best priced quote.

    Args:
        input_mint (str):
        output_mint (str):
        amount (int):
        slippage_bps (Union[Unset, None, int]):
        swap_mode (Union[Unset, None, GetQuoteSwapMode]):
        exclude_dexes (Union[Unset, None, List[GetQuoteExcludeDexesItem]]):
        only_direct_routes (Union[Unset, None, bool]):
        as_legacy_transaction (Union[Unset, None, bool]):
        platform_fee_bps (Union[Unset, None, int]):
        max_accounts (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QuoteResponse]
    """

    kwargs = _get_kwargs(
        input_mint=input_mint,
        output_mint=output_mint,
        amount=amount,
        slippage_bps=slippage_bps,
        swap_mode=swap_mode,
        exclude_dexes=exclude_dexes,
        only_direct_routes=only_direct_routes,
        as_legacy_transaction=as_legacy_transaction,
        platform_fee_bps=platform_fee_bps,
        max_accounts=max_accounts,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    input_mint: str,
    output_mint: str,
    amount: int,
    slippage_bps: Union[Unset, None, int] = UNSET,
    swap_mode: Union[Unset, None, GetQuoteSwapMode] = UNSET,
    exclude_dexes: Union[Unset, None, List[GetQuoteExcludeDexesItem]] = UNSET,
    only_direct_routes: Union[Unset, None, bool] = UNSET,
    as_legacy_transaction: Union[Unset, None, bool] = UNSET,
    platform_fee_bps: Union[Unset, None, int] = UNSET,
    max_accounts: Union[Unset, None, int] = UNSET,
) -> Optional[QuoteResponse]:
    """GET /quote

     Sends a GET request to the Jupiter API to get the best priced quote.

    Args:
        input_mint (str):
        output_mint (str):
        amount (int):
        slippage_bps (Union[Unset, None, int]):
        swap_mode (Union[Unset, None, GetQuoteSwapMode]):
        exclude_dexes (Union[Unset, None, List[GetQuoteExcludeDexesItem]]):
        only_direct_routes (Union[Unset, None, bool]):
        as_legacy_transaction (Union[Unset, None, bool]):
        platform_fee_bps (Union[Unset, None, int]):
        max_accounts (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QuoteResponse
    """

    return sync_detailed(
        client=client,
        input_mint=input_mint,
        output_mint=output_mint,
        amount=amount,
        slippage_bps=slippage_bps,
        swap_mode=swap_mode,
        exclude_dexes=exclude_dexes,
        only_direct_routes=only_direct_routes,
        as_legacy_transaction=as_legacy_transaction,
        platform_fee_bps=platform_fee_bps,
        max_accounts=max_accounts,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    input_mint: str,
    output_mint: str,
    amount: int,
    slippage_bps: Union[Unset, None, int] = UNSET,
    swap_mode: Union[Unset, None, GetQuoteSwapMode] = UNSET,
    exclude_dexes: Union[Unset, None, List[GetQuoteExcludeDexesItem]] = UNSET,
    only_direct_routes: Union[Unset, None, bool] = UNSET,
    as_legacy_transaction: Union[Unset, None, bool] = UNSET,
    platform_fee_bps: Union[Unset, None, int] = UNSET,
    max_accounts: Union[Unset, None, int] = UNSET,
) -> Response[QuoteResponse]:
    """GET /quote

     Sends a GET request to the Jupiter API to get the best priced quote.

    Args:
        input_mint (str):
        output_mint (str):
        amount (int):
        slippage_bps (Union[Unset, None, int]):
        swap_mode (Union[Unset, None, GetQuoteSwapMode]):
        exclude_dexes (Union[Unset, None, List[GetQuoteExcludeDexesItem]]):
        only_direct_routes (Union[Unset, None, bool]):
        as_legacy_transaction (Union[Unset, None, bool]):
        platform_fee_bps (Union[Unset, None, int]):
        max_accounts (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QuoteResponse]
    """

    kwargs = _get_kwargs(
        input_mint=input_mint,
        output_mint=output_mint,
        amount=amount,
        slippage_bps=slippage_bps,
        swap_mode=swap_mode,
        exclude_dexes=exclude_dexes,
        only_direct_routes=only_direct_routes,
        as_legacy_transaction=as_legacy_transaction,
        platform_fee_bps=platform_fee_bps,
        max_accounts=max_accounts,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    input_mint: str,
    output_mint: str,
    amount: int,
    slippage_bps: Union[Unset, None, int] = UNSET,
    swap_mode: Union[Unset, None, GetQuoteSwapMode] = UNSET,
    exclude_dexes: Union[Unset, None, List[GetQuoteExcludeDexesItem]] = UNSET,
    only_direct_routes: Union[Unset, None, bool] = UNSET,
    as_legacy_transaction: Union[Unset, None, bool] = UNSET,
    platform_fee_bps: Union[Unset, None, int] = UNSET,
    max_accounts: Union[Unset, None, int] = UNSET,
) -> Optional[QuoteResponse]:
    """GET /quote

     Sends a GET request to the Jupiter API to get the best priced quote.

    Args:
        input_mint (str):
        output_mint (str):
        amount (int):
        slippage_bps (Union[Unset, None, int]):
        swap_mode (Union[Unset, None, GetQuoteSwapMode]):
        exclude_dexes (Union[Unset, None, List[GetQuoteExcludeDexesItem]]):
        only_direct_routes (Union[Unset, None, bool]):
        as_legacy_transaction (Union[Unset, None, bool]):
        platform_fee_bps (Union[Unset, None, int]):
        max_accounts (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QuoteResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            input_mint=input_mint,
            output_mint=output_mint,
            amount=amount,
            slippage_bps=slippage_bps,
            swap_mode=swap_mode,
            exclude_dexes=exclude_dexes,
            only_direct_routes=only_direct_routes,
            as_legacy_transaction=as_legacy_transaction,
            platform_fee_bps=platform_fee_bps,
            max_accounts=max_accounts,
        )
    ).parsed

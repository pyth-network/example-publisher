from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_program_id_to_label_response_200 import GetProgramIdToLabelResponse200
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/program-id-to-label",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetProgramIdToLabelResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetProgramIdToLabelResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetProgramIdToLabelResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetProgramIdToLabelResponse200]:
    """GET /program-id-to-label

     Returns a hash, which key is the program id and value is the label. This is used to help map error
    from transaction by identifying the fault program id. With that, we can use the `excludeDexes` or
    `dexes` parameter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProgramIdToLabelResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetProgramIdToLabelResponse200]:
    """GET /program-id-to-label

     Returns a hash, which key is the program id and value is the label. This is used to help map error
    from transaction by identifying the fault program id. With that, we can use the `excludeDexes` or
    `dexes` parameter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetProgramIdToLabelResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetProgramIdToLabelResponse200]:
    """GET /program-id-to-label

     Returns a hash, which key is the program id and value is the label. This is used to help map error
    from transaction by identifying the fault program id. With that, we can use the `excludeDexes` or
    `dexes` parameter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProgramIdToLabelResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetProgramIdToLabelResponse200]:
    """GET /program-id-to-label

     Returns a hash, which key is the program id and value is the label. This is used to help map error
    from transaction by identifying the fault program id. With that, we can use the `excludeDexes` or
    `dexes` parameter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetProgramIdToLabelResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

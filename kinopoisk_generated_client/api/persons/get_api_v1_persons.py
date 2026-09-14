from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.person_by_name_response import PersonByNameResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    name: str,
    page: int | Unset = 1,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["name"] = name

    params["page"] = page


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/persons",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | PersonByNameResponse | None:
    if response.status_code == 200:
        response_200 = PersonByNameResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 402:
        response_402 = cast(Any, None)
        return response_402

    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | PersonByNameResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    name: str,
    page: int | Unset = 1,

) -> Response[Any | PersonByNameResponse]:
    """ поиск актеров, режиссеров и т.д. по имени

     Одна страница может содержать до 50 элементов в items.

    Args:
        name (str):
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PersonByNameResponse]
     """


    kwargs = _get_kwargs(
        name=name,
page=page,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    name: str,
    page: int | Unset = 1,

) -> Any | PersonByNameResponse | None:
    """ поиск актеров, режиссеров и т.д. по имени

     Одна страница может содержать до 50 элементов в items.

    Args:
        name (str):
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PersonByNameResponse
     """


    return sync_detailed(
        client=client,
name=name,
page=page,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    name: str,
    page: int | Unset = 1,

) -> Response[Any | PersonByNameResponse]:
    """ поиск актеров, режиссеров и т.д. по имени

     Одна страница может содержать до 50 элементов в items.

    Args:
        name (str):
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PersonByNameResponse]
     """


    kwargs = _get_kwargs(
        name=name,
page=page,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    name: str,
    page: int | Unset = 1,

) -> Any | PersonByNameResponse | None:
    """ поиск актеров, режиссеров и т.д. по имени

     Одна страница может содержать до 50 элементов в items.

    Args:
        name (str):
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PersonByNameResponse
     """


    return (await asyncio_detailed(
        client=client,
name=name,
page=page,

    )).parsed

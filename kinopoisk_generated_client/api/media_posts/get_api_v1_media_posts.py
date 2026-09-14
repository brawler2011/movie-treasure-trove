from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.media_posts_response import MediaPostsResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    page: int | Unset = 1,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/media_posts",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | MediaPostsResponse | None:
    if response.status_code == 200:
        response_200 = MediaPostsResponse.from_dict(response.json())



        return response_200

    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | MediaPostsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,

) -> Response[Any | MediaPostsResponse]:
    """ получить медиа новости с сайта кинопоиск

     Одна страница может содержать до 20 элементов в items.

    Args:
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | MediaPostsResponse]
     """


    kwargs = _get_kwargs(
        page=page,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,

) -> Any | MediaPostsResponse | None:
    """ получить медиа новости с сайта кинопоиск

     Одна страница может содержать до 20 элементов в items.

    Args:
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | MediaPostsResponse
     """


    return sync_detailed(
        client=client,
page=page,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,

) -> Response[Any | MediaPostsResponse]:
    """ получить медиа новости с сайта кинопоиск

     Одна страница может содержать до 20 элементов в items.

    Args:
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | MediaPostsResponse]
     """


    kwargs = _get_kwargs(
        page=page,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,

) -> Any | MediaPostsResponse | None:
    """ получить медиа новости с сайта кинопоиск

     Одна страница может содержать до 20 элементов в items.

    Args:
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | MediaPostsResponse
     """


    return (await asyncio_detailed(
        client=client,
page=page,

    )).parsed

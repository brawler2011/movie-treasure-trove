from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.film_collection_response import FilmCollectionResponse
from ...models.get_api_v22_films_collections_type import GetApiV22FilmsCollectionsType
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    type_: GetApiV22FilmsCollectionsType | Unset = GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL,
    page: int | Unset = 1,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_type_: str | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params["page"] = page


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2.2/films/collections",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | FilmCollectionResponse | None:
    if response.status_code == 200:
        response_200 = FilmCollectionResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | FilmCollectionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    type_: GetApiV22FilmsCollectionsType | Unset = GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL,
    page: int | Unset = 1,

) -> Response[Any | FilmCollectionResponse]:
    """ получить список фильмов из различных топов или коллекций. Например
    https://www.kinopoisk.ru/top/lists/58/

     Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов.

    Args:
        type_ (GetApiV22FilmsCollectionsType | Unset):  Default:
            GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL.
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | FilmCollectionResponse]
     """


    kwargs = _get_kwargs(
        type_=type_,
page=page,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    type_: GetApiV22FilmsCollectionsType | Unset = GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL,
    page: int | Unset = 1,

) -> Any | FilmCollectionResponse | None:
    """ получить список фильмов из различных топов или коллекций. Например
    https://www.kinopoisk.ru/top/lists/58/

     Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов.

    Args:
        type_ (GetApiV22FilmsCollectionsType | Unset):  Default:
            GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL.
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | FilmCollectionResponse
     """


    return sync_detailed(
        client=client,
type_=type_,
page=page,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    type_: GetApiV22FilmsCollectionsType | Unset = GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL,
    page: int | Unset = 1,

) -> Response[Any | FilmCollectionResponse]:
    """ получить список фильмов из различных топов или коллекций. Например
    https://www.kinopoisk.ru/top/lists/58/

     Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов.

    Args:
        type_ (GetApiV22FilmsCollectionsType | Unset):  Default:
            GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL.
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | FilmCollectionResponse]
     """


    kwargs = _get_kwargs(
        type_=type_,
page=page,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    type_: GetApiV22FilmsCollectionsType | Unset = GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL,
    page: int | Unset = 1,

) -> Any | FilmCollectionResponse | None:
    """ получить список фильмов из различных топов или коллекций. Например
    https://www.kinopoisk.ru/top/lists/58/

     Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов.

    Args:
        type_ (GetApiV22FilmsCollectionsType | Unset):  Default:
            GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL.
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | FilmCollectionResponse
     """


    return (await asyncio_detailed(
        client=client,
type_=type_,
page=page,

    )).parsed

from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_api_v22_films_premieres_month import GetApiV22FilmsPremieresMonth
from ...models.premiere_response import PremiereResponse
from typing import cast



def _get_kwargs(
    *,
    year: int,
    month: GetApiV22FilmsPremieresMonth,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["year"] = year

    json_month = month.value
    params["month"] = json_month


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2.2/films/premieres",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | PremiereResponse | None:
    if response.status_code == 200:
        response_200 = PremiereResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | PremiereResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    year: int,
    month: GetApiV22FilmsPremieresMonth,

) -> Response[Any | PremiereResponse]:
    """ получить список кинопремьер

     Данный эндпоинт возвращает список кинопремьер. Например https://www.kinopoisk.ru/premiere/

    Args:
        year (int):
        month (GetApiV22FilmsPremieresMonth):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PremiereResponse]
     """


    kwargs = _get_kwargs(
        year=year,
month=month,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    year: int,
    month: GetApiV22FilmsPremieresMonth,

) -> Any | PremiereResponse | None:
    """ получить список кинопремьер

     Данный эндпоинт возвращает список кинопремьер. Например https://www.kinopoisk.ru/premiere/

    Args:
        year (int):
        month (GetApiV22FilmsPremieresMonth):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PremiereResponse
     """


    return sync_detailed(
        client=client,
year=year,
month=month,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    year: int,
    month: GetApiV22FilmsPremieresMonth,

) -> Response[Any | PremiereResponse]:
    """ получить список кинопремьер

     Данный эндпоинт возвращает список кинопремьер. Например https://www.kinopoisk.ru/premiere/

    Args:
        year (int):
        month (GetApiV22FilmsPremieresMonth):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PremiereResponse]
     """


    kwargs = _get_kwargs(
        year=year,
month=month,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    year: int,
    month: GetApiV22FilmsPremieresMonth,

) -> Any | PremiereResponse | None:
    """ получить список кинопремьер

     Данный эндпоинт возвращает список кинопремьер. Например https://www.kinopoisk.ru/premiere/

    Args:
        year (int):
        month (GetApiV22FilmsPremieresMonth):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PremiereResponse
     """


    return (await asyncio_detailed(
        client=client,
year=year,
month=month,

    )).parsed

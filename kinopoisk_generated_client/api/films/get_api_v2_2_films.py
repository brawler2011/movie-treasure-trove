from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.film_search_by_filters_response import FilmSearchByFiltersResponse
from ...models.get_api_v22_films_order import GetApiV22FilmsOrder
from ...models.get_api_v22_films_type import GetApiV22FilmsType
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    countries: list[int] | Unset = UNSET,
    genres: list[int] | Unset = UNSET,
    order: GetApiV22FilmsOrder | Unset = GetApiV22FilmsOrder.RATING,
    type_: GetApiV22FilmsType | Unset = GetApiV22FilmsType.ALL,
    rating_from: float | Unset = 0.0,
    rating_to: float | Unset = 10.0,
    year_from: int | Unset = 1000,
    year_to: int | Unset = 3000,
    imdb_id: str | Unset = UNSET,
    keyword: str | Unset = UNSET,
    page: int | Unset = 1,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_countries: list[int] | Unset = UNSET
    if not isinstance(countries, Unset):
        json_countries = countries


    params["countries"] = json_countries

    json_genres: list[int] | Unset = UNSET
    if not isinstance(genres, Unset):
        json_genres = genres


    params["genres"] = json_genres

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    json_type_: str | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params["ratingFrom"] = rating_from

    params["ratingTo"] = rating_to

    params["yearFrom"] = year_from

    params["yearTo"] = year_to

    params["imdbId"] = imdb_id

    params["keyword"] = keyword

    params["page"] = page


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2.2/films",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | FilmSearchByFiltersResponse | None:
    if response.status_code == 200:
        response_200 = FilmSearchByFiltersResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | FilmSearchByFiltersResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    countries: list[int] | Unset = UNSET,
    genres: list[int] | Unset = UNSET,
    order: GetApiV22FilmsOrder | Unset = GetApiV22FilmsOrder.RATING,
    type_: GetApiV22FilmsType | Unset = GetApiV22FilmsType.ALL,
    rating_from: float | Unset = 0.0,
    rating_to: float | Unset = 10.0,
    year_from: int | Unset = 1000,
    year_to: int | Unset = 3000,
    imdb_id: str | Unset = UNSET,
    keyword: str | Unset = UNSET,
    page: int | Unset = 1,

) -> Response[Any | FilmSearchByFiltersResponse]:
    """ получить список фильмов по различным фильтрам

     Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов. Данный
    эндпоинт не возращает более 400 фильмов. <i>Используй /api/v2.2/films/filters чтобы получить id
    стран и жанров.</i>

    Args:
        countries (list[int] | Unset):
        genres (list[int] | Unset):
        order (GetApiV22FilmsOrder | Unset):  Default: GetApiV22FilmsOrder.RATING.
        type_ (GetApiV22FilmsType | Unset):  Default: GetApiV22FilmsType.ALL.
        rating_from (float | Unset):  Default: 0.0.
        rating_to (float | Unset):  Default: 10.0.
        year_from (int | Unset):  Default: 1000.
        year_to (int | Unset):  Default: 3000.
        imdb_id (str | Unset):
        keyword (str | Unset):
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | FilmSearchByFiltersResponse]
     """


    kwargs = _get_kwargs(
        countries=countries,
genres=genres,
order=order,
type_=type_,
rating_from=rating_from,
rating_to=rating_to,
year_from=year_from,
year_to=year_to,
imdb_id=imdb_id,
keyword=keyword,
page=page,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    countries: list[int] | Unset = UNSET,
    genres: list[int] | Unset = UNSET,
    order: GetApiV22FilmsOrder | Unset = GetApiV22FilmsOrder.RATING,
    type_: GetApiV22FilmsType | Unset = GetApiV22FilmsType.ALL,
    rating_from: float | Unset = 0.0,
    rating_to: float | Unset = 10.0,
    year_from: int | Unset = 1000,
    year_to: int | Unset = 3000,
    imdb_id: str | Unset = UNSET,
    keyword: str | Unset = UNSET,
    page: int | Unset = 1,

) -> Any | FilmSearchByFiltersResponse | None:
    """ получить список фильмов по различным фильтрам

     Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов. Данный
    эндпоинт не возращает более 400 фильмов. <i>Используй /api/v2.2/films/filters чтобы получить id
    стран и жанров.</i>

    Args:
        countries (list[int] | Unset):
        genres (list[int] | Unset):
        order (GetApiV22FilmsOrder | Unset):  Default: GetApiV22FilmsOrder.RATING.
        type_ (GetApiV22FilmsType | Unset):  Default: GetApiV22FilmsType.ALL.
        rating_from (float | Unset):  Default: 0.0.
        rating_to (float | Unset):  Default: 10.0.
        year_from (int | Unset):  Default: 1000.
        year_to (int | Unset):  Default: 3000.
        imdb_id (str | Unset):
        keyword (str | Unset):
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | FilmSearchByFiltersResponse
     """


    return sync_detailed(
        client=client,
countries=countries,
genres=genres,
order=order,
type_=type_,
rating_from=rating_from,
rating_to=rating_to,
year_from=year_from,
year_to=year_to,
imdb_id=imdb_id,
keyword=keyword,
page=page,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    countries: list[int] | Unset = UNSET,
    genres: list[int] | Unset = UNSET,
    order: GetApiV22FilmsOrder | Unset = GetApiV22FilmsOrder.RATING,
    type_: GetApiV22FilmsType | Unset = GetApiV22FilmsType.ALL,
    rating_from: float | Unset = 0.0,
    rating_to: float | Unset = 10.0,
    year_from: int | Unset = 1000,
    year_to: int | Unset = 3000,
    imdb_id: str | Unset = UNSET,
    keyword: str | Unset = UNSET,
    page: int | Unset = 1,

) -> Response[Any | FilmSearchByFiltersResponse]:
    """ получить список фильмов по различным фильтрам

     Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов. Данный
    эндпоинт не возращает более 400 фильмов. <i>Используй /api/v2.2/films/filters чтобы получить id
    стран и жанров.</i>

    Args:
        countries (list[int] | Unset):
        genres (list[int] | Unset):
        order (GetApiV22FilmsOrder | Unset):  Default: GetApiV22FilmsOrder.RATING.
        type_ (GetApiV22FilmsType | Unset):  Default: GetApiV22FilmsType.ALL.
        rating_from (float | Unset):  Default: 0.0.
        rating_to (float | Unset):  Default: 10.0.
        year_from (int | Unset):  Default: 1000.
        year_to (int | Unset):  Default: 3000.
        imdb_id (str | Unset):
        keyword (str | Unset):
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | FilmSearchByFiltersResponse]
     """


    kwargs = _get_kwargs(
        countries=countries,
genres=genres,
order=order,
type_=type_,
rating_from=rating_from,
rating_to=rating_to,
year_from=year_from,
year_to=year_to,
imdb_id=imdb_id,
keyword=keyword,
page=page,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    countries: list[int] | Unset = UNSET,
    genres: list[int] | Unset = UNSET,
    order: GetApiV22FilmsOrder | Unset = GetApiV22FilmsOrder.RATING,
    type_: GetApiV22FilmsType | Unset = GetApiV22FilmsType.ALL,
    rating_from: float | Unset = 0.0,
    rating_to: float | Unset = 10.0,
    year_from: int | Unset = 1000,
    year_to: int | Unset = 3000,
    imdb_id: str | Unset = UNSET,
    keyword: str | Unset = UNSET,
    page: int | Unset = 1,

) -> Any | FilmSearchByFiltersResponse | None:
    """ получить список фильмов по различным фильтрам

     Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов. Данный
    эндпоинт не возращает более 400 фильмов. <i>Используй /api/v2.2/films/filters чтобы получить id
    стран и жанров.</i>

    Args:
        countries (list[int] | Unset):
        genres (list[int] | Unset):
        order (GetApiV22FilmsOrder | Unset):  Default: GetApiV22FilmsOrder.RATING.
        type_ (GetApiV22FilmsType | Unset):  Default: GetApiV22FilmsType.ALL.
        rating_from (float | Unset):  Default: 0.0.
        rating_to (float | Unset):  Default: 10.0.
        year_from (int | Unset):  Default: 1000.
        year_to (int | Unset):  Default: 3000.
        imdb_id (str | Unset):
        keyword (str | Unset):
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | FilmSearchByFiltersResponse
     """


    return (await asyncio_detailed(
        client=client,
countries=countries,
genres=genres,
order=order,
type_=type_,
rating_from=rating_from,
rating_to=rating_to,
year_from=year_from,
year_to=year_to,
imdb_id=imdb_id,
keyword=keyword,
page=page,

    )).parsed

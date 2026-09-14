from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_api_v22_films_id_reviews_order import GetApiV22FilmsIdReviewsOrder
from ...models.review_response import ReviewResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    id: int,
    *,
    page: int | Unset = 1,
    order: GetApiV22FilmsIdReviewsOrder | Unset = GetApiV22FilmsIdReviewsOrder.DATE_DESC,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2.2/films/{id}/reviews".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ReviewResponse | None:
    if response.status_code == 200:
        response_200 = ReviewResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ReviewResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,
    order: GetApiV22FilmsIdReviewsOrder | Unset = GetApiV22FilmsIdReviewsOrder.DATE_DESC,

) -> Response[Any | ReviewResponse]:
    """ получить список рецензии зрителей по kinopoisk film id

     Возвращает список рецензии зрителей с пагинацией. Каждая страница содержит не более чем 20 рецензий.

    Args:
        id (int):
        page (int | Unset):  Default: 1.
        order (GetApiV22FilmsIdReviewsOrder | Unset):  Default:
            GetApiV22FilmsIdReviewsOrder.DATE_DESC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ReviewResponse]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
order=order,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,
    order: GetApiV22FilmsIdReviewsOrder | Unset = GetApiV22FilmsIdReviewsOrder.DATE_DESC,

) -> Any | ReviewResponse | None:
    """ получить список рецензии зрителей по kinopoisk film id

     Возвращает список рецензии зрителей с пагинацией. Каждая страница содержит не более чем 20 рецензий.

    Args:
        id (int):
        page (int | Unset):  Default: 1.
        order (GetApiV22FilmsIdReviewsOrder | Unset):  Default:
            GetApiV22FilmsIdReviewsOrder.DATE_DESC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ReviewResponse
     """


    return sync_detailed(
        id=id,
client=client,
page=page,
order=order,

    ).parsed

async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,
    order: GetApiV22FilmsIdReviewsOrder | Unset = GetApiV22FilmsIdReviewsOrder.DATE_DESC,

) -> Response[Any | ReviewResponse]:
    """ получить список рецензии зрителей по kinopoisk film id

     Возвращает список рецензии зрителей с пагинацией. Каждая страница содержит не более чем 20 рецензий.

    Args:
        id (int):
        page (int | Unset):  Default: 1.
        order (GetApiV22FilmsIdReviewsOrder | Unset):  Default:
            GetApiV22FilmsIdReviewsOrder.DATE_DESC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ReviewResponse]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
order=order,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,
    order: GetApiV22FilmsIdReviewsOrder | Unset = GetApiV22FilmsIdReviewsOrder.DATE_DESC,

) -> Any | ReviewResponse | None:
    """ получить список рецензии зрителей по kinopoisk film id

     Возвращает список рецензии зрителей с пагинацией. Каждая страница содержит не более чем 20 рецензий.

    Args:
        id (int):
        page (int | Unset):  Default: 1.
        order (GetApiV22FilmsIdReviewsOrder | Unset):  Default:
            GetApiV22FilmsIdReviewsOrder.DATE_DESC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ReviewResponse
     """


    return (await asyncio_detailed(
        id=id,
client=client,
page=page,
order=order,

    )).parsed

from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_api_v22_films_id_images_type import GetApiV22FilmsIdImagesType
from ...models.image_response import ImageResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    id: int,
    *,
    type_: GetApiV22FilmsIdImagesType | Unset = GetApiV22FilmsIdImagesType.STILL,
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
        "url": "/api/v2.2/films/{id}/images".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ImageResponse | None:
    if response.status_code == 200:
        response_200 = ImageResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ImageResponse]:
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
    type_: GetApiV22FilmsIdImagesType | Unset = GetApiV22FilmsIdImagesType.STILL,
    page: int | Unset = 1,

) -> Response[Any | ImageResponse]:
    """ получить изображения(кадры, постеры, фан-арты, обои и т.д.) связанные с фильмом по kinopoisk film id

     Данный эндпоинт возвращает изображения связанные с фильмом с пагинацией. Каждая страница содержит
    <b>не более чем 20 фильмов</b>.</br> Доступные изображения:</br> <ul> <li>STILL - кадры</li>
    <li>SHOOTING - изображения со съемок</li> <li>POSTER - постеры</li> <li>FAN_ART - фан-арты</li>
    <li>PROMO - промо</li> <li>CONCEPT - концепт-арты</li> <li>WALLPAPER - обои</li> <li>COVER -
    обложки</li> <li>SCREENSHOT - скриншоты</li> </ul>

    Args:
        id (int):
        type_ (GetApiV22FilmsIdImagesType | Unset):  Default: GetApiV22FilmsIdImagesType.STILL.
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ImageResponse]
     """


    kwargs = _get_kwargs(
        id=id,
type_=type_,
page=page,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    type_: GetApiV22FilmsIdImagesType | Unset = GetApiV22FilmsIdImagesType.STILL,
    page: int | Unset = 1,

) -> Any | ImageResponse | None:
    """ получить изображения(кадры, постеры, фан-арты, обои и т.д.) связанные с фильмом по kinopoisk film id

     Данный эндпоинт возвращает изображения связанные с фильмом с пагинацией. Каждая страница содержит
    <b>не более чем 20 фильмов</b>.</br> Доступные изображения:</br> <ul> <li>STILL - кадры</li>
    <li>SHOOTING - изображения со съемок</li> <li>POSTER - постеры</li> <li>FAN_ART - фан-арты</li>
    <li>PROMO - промо</li> <li>CONCEPT - концепт-арты</li> <li>WALLPAPER - обои</li> <li>COVER -
    обложки</li> <li>SCREENSHOT - скриншоты</li> </ul>

    Args:
        id (int):
        type_ (GetApiV22FilmsIdImagesType | Unset):  Default: GetApiV22FilmsIdImagesType.STILL.
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ImageResponse
     """


    return sync_detailed(
        id=id,
client=client,
type_=type_,
page=page,

    ).parsed

async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    type_: GetApiV22FilmsIdImagesType | Unset = GetApiV22FilmsIdImagesType.STILL,
    page: int | Unset = 1,

) -> Response[Any | ImageResponse]:
    """ получить изображения(кадры, постеры, фан-арты, обои и т.д.) связанные с фильмом по kinopoisk film id

     Данный эндпоинт возвращает изображения связанные с фильмом с пагинацией. Каждая страница содержит
    <b>не более чем 20 фильмов</b>.</br> Доступные изображения:</br> <ul> <li>STILL - кадры</li>
    <li>SHOOTING - изображения со съемок</li> <li>POSTER - постеры</li> <li>FAN_ART - фан-арты</li>
    <li>PROMO - промо</li> <li>CONCEPT - концепт-арты</li> <li>WALLPAPER - обои</li> <li>COVER -
    обложки</li> <li>SCREENSHOT - скриншоты</li> </ul>

    Args:
        id (int):
        type_ (GetApiV22FilmsIdImagesType | Unset):  Default: GetApiV22FilmsIdImagesType.STILL.
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ImageResponse]
     """


    kwargs = _get_kwargs(
        id=id,
type_=type_,
page=page,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    type_: GetApiV22FilmsIdImagesType | Unset = GetApiV22FilmsIdImagesType.STILL,
    page: int | Unset = 1,

) -> Any | ImageResponse | None:
    """ получить изображения(кадры, постеры, фан-арты, обои и т.д.) связанные с фильмом по kinopoisk film id

     Данный эндпоинт возвращает изображения связанные с фильмом с пагинацией. Каждая страница содержит
    <b>не более чем 20 фильмов</b>.</br> Доступные изображения:</br> <ul> <li>STILL - кадры</li>
    <li>SHOOTING - изображения со съемок</li> <li>POSTER - постеры</li> <li>FAN_ART - фан-арты</li>
    <li>PROMO - промо</li> <li>CONCEPT - концепт-арты</li> <li>WALLPAPER - обои</li> <li>COVER -
    обложки</li> <li>SCREENSHOT - скриншоты</li> </ul>

    Args:
        id (int):
        type_ (GetApiV22FilmsIdImagesType | Unset):  Default: GetApiV22FilmsIdImagesType.STILL.
        page (int | Unset):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ImageResponse
     """


    return (await asyncio_detailed(
        id=id,
client=client,
type_=type_,
page=page,

    )).parsed

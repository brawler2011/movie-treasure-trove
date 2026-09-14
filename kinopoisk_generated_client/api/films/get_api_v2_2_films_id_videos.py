from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.video_response import VideoResponse
from typing import cast



def _get_kwargs(
    id: int,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2.2/films/{id}/videos".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | VideoResponse | None:
    if response.status_code == 200:
        response_200 = VideoResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | VideoResponse]:
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

) -> Response[Any | VideoResponse]:
    """ получить трейлеры,тизеры,видео для фильма по kinopoisk film id

     Данный эндпоинт возвращает трейлеры,тизеры,видео для фильма по kinopoisk film id. В данный момент
    доступно три site:  <br/> <ul><li>YOUTUBE - в этом случае <b>url</b> это просто ссылка на youtube
    видео.</li><li>YANDEX_DISK - в этом случае <b>url</b> это ссылка на yandex
    disk.</li><li>KINOPOISK_WIDGET - в этом случае <b>url</b> это ссылка на кинопоиск виджет. <b>Видео
    доступно только с РФ ip</b>. Например
    https://widgets.kinopoisk.ru/discovery/trailer/123573?onlyPlayer=1&autoplay=1&cover=1. Если вы
    хотите вставить этот виджет на вашу страницу, вы можете сделать следующее:  <br/><br/>&lt;script
    src=&quot;https://unpkg.com/@ungap/custom-elements-builtin&quot;&gt;&lt;/script&gt;<br/>&lt;script
    type=&quot;module&quot; src=&quot;https://unpkg.com/x-frame-
    bypass&quot;&gt;&lt;/script&gt;<br/>&lt;iframe is=&quot;x-frame-bypass&quot; src=&quot;https://widge
    ts.kinopoisk.ru/discovery/trailer/167560?onlyPlayer=1&amp;autoplay=1&amp;cover=1&quot;
    width=&quot;500&quot; height=&quot;500&quot;&gt;&lt;/iframe&gt;</li></ul>

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | VideoResponse]
     """


    kwargs = _get_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: int,
    *,
    client: AuthenticatedClient | Client,

) -> Any | VideoResponse | None:
    """ получить трейлеры,тизеры,видео для фильма по kinopoisk film id

     Данный эндпоинт возвращает трейлеры,тизеры,видео для фильма по kinopoisk film id. В данный момент
    доступно три site:  <br/> <ul><li>YOUTUBE - в этом случае <b>url</b> это просто ссылка на youtube
    видео.</li><li>YANDEX_DISK - в этом случае <b>url</b> это ссылка на yandex
    disk.</li><li>KINOPOISK_WIDGET - в этом случае <b>url</b> это ссылка на кинопоиск виджет. <b>Видео
    доступно только с РФ ip</b>. Например
    https://widgets.kinopoisk.ru/discovery/trailer/123573?onlyPlayer=1&autoplay=1&cover=1. Если вы
    хотите вставить этот виджет на вашу страницу, вы можете сделать следующее:  <br/><br/>&lt;script
    src=&quot;https://unpkg.com/@ungap/custom-elements-builtin&quot;&gt;&lt;/script&gt;<br/>&lt;script
    type=&quot;module&quot; src=&quot;https://unpkg.com/x-frame-
    bypass&quot;&gt;&lt;/script&gt;<br/>&lt;iframe is=&quot;x-frame-bypass&quot; src=&quot;https://widge
    ts.kinopoisk.ru/discovery/trailer/167560?onlyPlayer=1&amp;autoplay=1&amp;cover=1&quot;
    width=&quot;500&quot; height=&quot;500&quot;&gt;&lt;/iframe&gt;</li></ul>

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | VideoResponse
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | VideoResponse]:
    """ получить трейлеры,тизеры,видео для фильма по kinopoisk film id

     Данный эндпоинт возвращает трейлеры,тизеры,видео для фильма по kinopoisk film id. В данный момент
    доступно три site:  <br/> <ul><li>YOUTUBE - в этом случае <b>url</b> это просто ссылка на youtube
    видео.</li><li>YANDEX_DISK - в этом случае <b>url</b> это ссылка на yandex
    disk.</li><li>KINOPOISK_WIDGET - в этом случае <b>url</b> это ссылка на кинопоиск виджет. <b>Видео
    доступно только с РФ ip</b>. Например
    https://widgets.kinopoisk.ru/discovery/trailer/123573?onlyPlayer=1&autoplay=1&cover=1. Если вы
    хотите вставить этот виджет на вашу страницу, вы можете сделать следующее:  <br/><br/>&lt;script
    src=&quot;https://unpkg.com/@ungap/custom-elements-builtin&quot;&gt;&lt;/script&gt;<br/>&lt;script
    type=&quot;module&quot; src=&quot;https://unpkg.com/x-frame-
    bypass&quot;&gt;&lt;/script&gt;<br/>&lt;iframe is=&quot;x-frame-bypass&quot; src=&quot;https://widge
    ts.kinopoisk.ru/discovery/trailer/167560?onlyPlayer=1&amp;autoplay=1&amp;cover=1&quot;
    width=&quot;500&quot; height=&quot;500&quot;&gt;&lt;/iframe&gt;</li></ul>

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | VideoResponse]
     """


    kwargs = _get_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient | Client,

) -> Any | VideoResponse | None:
    """ получить трейлеры,тизеры,видео для фильма по kinopoisk film id

     Данный эндпоинт возвращает трейлеры,тизеры,видео для фильма по kinopoisk film id. В данный момент
    доступно три site:  <br/> <ul><li>YOUTUBE - в этом случае <b>url</b> это просто ссылка на youtube
    видео.</li><li>YANDEX_DISK - в этом случае <b>url</b> это ссылка на yandex
    disk.</li><li>KINOPOISK_WIDGET - в этом случае <b>url</b> это ссылка на кинопоиск виджет. <b>Видео
    доступно только с РФ ip</b>. Например
    https://widgets.kinopoisk.ru/discovery/trailer/123573?onlyPlayer=1&autoplay=1&cover=1. Если вы
    хотите вставить этот виджет на вашу страницу, вы можете сделать следующее:  <br/><br/>&lt;script
    src=&quot;https://unpkg.com/@ungap/custom-elements-builtin&quot;&gt;&lt;/script&gt;<br/>&lt;script
    type=&quot;module&quot; src=&quot;https://unpkg.com/x-frame-
    bypass&quot;&gt;&lt;/script&gt;<br/>&lt;iframe is=&quot;x-frame-bypass&quot; src=&quot;https://widge
    ts.kinopoisk.ru/discovery/trailer/167560?onlyPlayer=1&amp;autoplay=1&amp;cover=1&quot;
    width=&quot;500&quot; height=&quot;500&quot;&gt;&lt;/iframe&gt;</li></ul>

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | VideoResponse
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed

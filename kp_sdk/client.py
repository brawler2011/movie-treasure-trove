import asyncio
import logging
import os
import time
from typing import Optional

from kinopoisk_generated_client.client import AuthenticatedClient
from kinopoisk_generated_client.api.films import (
    get_api_v2_2_films_collections,
    get_api_v2_2_films_id,
    get_api_v2_1_films_search_by_keyword,
)
from kinopoisk_generated_client.models.get_api_v22_films_collections_type import (
    GetApiV22FilmsCollectionsType,
)
from kinopoisk_generated_client.models.film_collection_response import (
    FilmCollectionResponse,
)
from kinopoisk_generated_client.models.film import Film
from kinopoisk_generated_client.models.film_search_response import (
    FilmSearchResponse,
)

logger = logging.getLogger(__name__)


class KinopoiskSDK:
    """
    Высокоуровневый асинхронный SDK для Kinopoisk Unofficial API
    с встроенным контролем частоты запросов (rate-limiting) и автоповтором при 429.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://kinopoiskapiunofficial.tech",
        requests_per_second: float = 15.0,
        max_retries: int = 4,
    ):
        self.api_key = api_key or os.getenv(
            "KINOPOISK_API_KEY", "71c5dd47-2ab2-40d4-bb00-4974097af5b6"
        )
        self.base_url = base_url
        self.min_interval = 1.0 / max(1.0, requests_per_second)
        self.max_retries = max_retries

        self._last_request_time = 0.0
        self._lock = asyncio.Lock()
        self._client: Optional[AuthenticatedClient] = None

    def _get_client(self) -> AuthenticatedClient:
        if self._client is None:
            self._client = AuthenticatedClient(
                base_url=self.base_url,
                token=self.api_key,
                auth_header_name="X-API-KEY",
                prefix="",
            )
        return self._client

    async def __aenter__(self):
        client = self._get_client()
        await client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def _rate_limit_wait(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_request_time
            if elapsed < self.min_interval:
                await asyncio.sleep(self.min_interval - elapsed)
            self._last_request_time = time.monotonic()

    async def _execute_with_retry(self, api_func, **kwargs):
        backoff = 1.0
        for attempt in range(self.max_retries + 1):
            await self._rate_limit_wait()
            try:
                result = await api_func.asyncio(client=self._get_client(), **kwargs)
                if result is not None:
                    return result
                # Если вернулся None (например, 429 или временная ошибка), делаем backoff
                if attempt < self.max_retries:
                    logger.warning(
                        "Пустой ответ или ограничение API, повтор через %.1f сек (попытка %d/%d)",
                        backoff,
                        attempt + 1,
                        self.max_retries,
                    )
                    await asyncio.sleep(backoff)
                    backoff *= 2.0
            except Exception as e:
                if attempt < self.max_retries:
                    logger.warning(
                        "Ошибка запроса: %s. Повтор через %.1f сек", e, backoff
                    )
                    await asyncio.sleep(backoff)
                    backoff *= 2.0
                else:
                    logger.error("Превышено количество попыток запроса: %s", e)
                    raise
        return None

    async def get_collection(
        self,
        collection_type: GetApiV22FilmsCollectionsType = GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL,
        page: int = 1,
    ) -> Optional[FilmCollectionResponse]:
        """Получить страницу подборки фильмов (TOP_250_MOVIES, TOP_POPULAR_ALL, etc.)"""
        return await self._execute_with_retry(
            get_api_v2_2_films_collections,
            type_=collection_type,
            page=page,
        )

    async def get_top_250(self, page: int = 1) -> Optional[FilmCollectionResponse]:
        return await self.get_collection(
            collection_type=GetApiV22FilmsCollectionsType.TOP_250_MOVIES, page=page
        )

    async def get_popular(self, page: int = 1) -> Optional[FilmCollectionResponse]:
        return await self.get_collection(
            collection_type=GetApiV22FilmsCollectionsType.TOP_POPULAR_ALL, page=page
        )

    async def get_film_details(self, film_id: int) -> Optional[Film]:
        """Получить детальную информацию о фильме по Kinopoisk ID"""
        return await self._execute_with_retry(
            get_api_v2_2_films_id,
            id=film_id,
        )

    async def search_by_keyword(
        self, keyword: str, page: int = 1
    ) -> Optional[FilmSearchResponse]:
        """Поиск фильмов по ключевому слову"""
        return await self._execute_with_retry(
            get_api_v2_1_films_search_by_keyword,
            keyword=keyword,
            page=page,
        )

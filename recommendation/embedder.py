import asyncio
import logging
import os
from typing import List, Optional, Union
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

_EMBEDDER_INSTANCE: Optional["MovieEmbedder"] = None


class MovieEmbedder:
    """
    Класс для вычисления локальных семантических эмбеддингов описаний и жанров фильмов.
    Использует сверхбыструю и точную модель cointegrated/rubert-tiny2 (~40 МБ, CPU < 10 мс).
    Настроен на строгое ограничение использования CPU на VPS.
    """

    def __init__(self, model_name: str = "cointegrated/rubert-tiny2"):
        self.model_name = model_name
        self._semaphore = asyncio.Semaphore(1)

        # Ограничиваем количество потоков PyTorch, чтобы не нагружать все ядра VPS
        cpu_threads = int(os.getenv("CPU_THREADS", os.getenv("TORCH_NUM_THREADS", "1")))
        torch.set_num_threads(cpu_threads)
        try:
            torch.set_num_interop_threads(1)
        except RuntimeError:
            pass

        logger.info(
            "Загрузка модели эмбеддингов %s (PyTorch threads: %d)...",
            model_name,
            torch.get_num_threads(),
        )
        self.model = SentenceTransformer(model_name)
        logger.info("Модель эмбеддингов готова.")

    @staticmethod
    def build_movie_text(
        name_ru: str,
        genres: List[str],
        year: Optional[int] = None,
        description: Optional[str] = None,
        short_description: Optional[str] = None,
    ) -> str:
        parts = [f"Фильм: {name_ru}"]
        if year:
            parts.append(f"Год: {year}")
        if genres:
            parts.append(f"Жанры: {', '.join(genres)}")
        if short_description and short_description.strip():
            parts.append(short_description.strip())
        elif description and description.strip():
            # Ограничиваем длину описания первыми 300 символами для фокуса на сути
            parts.append(description.strip()[:350])
        return ". ".join(parts)

    def encode_text(self, text: str) -> np.ndarray:
        embedding = self.model.encode(
            text, convert_to_numpy=True, normalize_embeddings=True
        )
        return embedding.astype(np.float32)

    async def encode_text_async(self, text: str) -> np.ndarray:
        """
        Асинхронная векторизация текста в отдельном потоке
        с защитой через Semaphore от одновременных вызовов.
        """
        async with self._semaphore:
            return await asyncio.to_thread(self.encode_text, text)

    def encode_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embeddings.astype(np.float32)

    async def encode_batch_async(
        self, texts: List[str], batch_size: int = 32
    ) -> np.ndarray:
        """
        Асинхронная батч-векторизация с семафором для минимизации нагрузки на CPU.
        """
        async with self._semaphore:
            return await asyncio.to_thread(self.encode_batch, texts, batch_size)


    @staticmethod
    def to_bytes(vector: np.ndarray) -> bytes:
        return vector.astype(np.float32).tobytes()

    @staticmethod
    def from_bytes(data: bytes) -> np.ndarray:
        return np.frombuffer(data, dtype=np.float32)


def get_embedder() -> MovieEmbedder:
    global _EMBEDDER_INSTANCE
    if _EMBEDDER_INSTANCE is None:
        _EMBEDDER_INSTANCE = MovieEmbedder()
    return _EMBEDDER_INSTANCE

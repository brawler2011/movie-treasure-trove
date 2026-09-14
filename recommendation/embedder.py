import logging
from typing import List, Optional, Union
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

_EMBEDDER_INSTANCE: Optional["MovieEmbedder"] = None


class MovieEmbedder:
    """
    Класс для вычисления локальных семантических эмбеддингов описаний и жанров фильмов.
    Использует сверхбыструю и точную модель cointegrated/rubert-tiny2 (~40 МБ, CPU < 10 мс).
    """

    def __init__(self, model_name: str = "cointegrated/rubert-tiny2"):
        self.model_name = model_name
        logger.info("Загрузка модели эмбеддингов %s...", model_name)
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

    def encode_batch(self, texts: List[str], batch_size: int = 64) -> np.ndarray:
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embeddings.astype(np.float32)

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

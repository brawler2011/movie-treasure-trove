import asyncio
import json
import logging
from typing import List, Optional, Set, Tuple
import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models import Movie, MovieEmbedding, UserInteraction, UserProfile
from database.session import async_session_factory
from recommendation.embedder import MovieEmbedder, get_embedder

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Рекомендательный движок на семантических эмбеддингах с динамическим дообучением (online centroid learning).
    Хранит векторную матрицу базы фильмов в оперативной памяти для мгновенного скоринга (< 5 мс).
    """

    def __init__(self):
        self.embedder = get_embedder()
        self._movie_ids: List[int] = []
        self._embedding_matrix: Optional[np.ndarray] = None  # shape: (N, dim)
        self._lock = asyncio.Lock()
        self._initialized = False

    async def reload_cache(self):
        """Загружает все векторы фильмов из БД в оперативную память"""
        async with self._lock:
            async with async_session_factory() as session:
                stmt = select(MovieEmbedding.movie_id, MovieEmbedding.embedding)
                result = await session.execute(stmt)
                rows = result.all()

                if not rows:
                    self._movie_ids = []
                    self._embedding_matrix = None
                    self._initialized = True
                    return

                movie_ids = []
                vectors = []
                for movie_id, emb_bytes in rows:
                    vec = MovieEmbedder.from_bytes(emb_bytes)
                    movie_ids.append(movie_id)
                    vectors.append(vec)

                self._movie_ids = movie_ids
                self._embedding_matrix = np.vstack(vectors)  # (N, 312)
                # Нормализуем строки для прямого скалярного произведения как косинуса
                norms = np.linalg.norm(self._embedding_matrix, axis=1, keepdims=True)
                norms[norms == 0] = 1.0
                self._embedding_matrix = self._embedding_matrix / norms
                self._initialized = True
                logger.info(
                    "Кэш векторов загружен: %d фильмов в памяти", len(self._movie_ids)
                )

    async def ensure_initialized(self):
        if not self._initialized:
            await self.reload_cache()

    async def add_movie_embedding(self, movie_id: int, vector: np.ndarray):
        """Динамически добавляет новый фильм в матрицу в памяти"""
        async with self._lock:
            norm = np.linalg.norm(vector)
            norm_vec = vector / (norm if norm > 0 else 1.0)
            if self._embedding_matrix is None or len(self._movie_ids) == 0:
                self._movie_ids = [movie_id]
                self._embedding_matrix = norm_vec.reshape(1, -1)
            else:
                if movie_id in self._movie_ids:
                    idx = self._movie_ids.index(movie_id)
                    self._embedding_matrix[idx] = norm_vec
                else:
                    self._movie_ids.append(movie_id)
                    self._embedding_matrix = np.vstack(
                        [self._embedding_matrix, norm_vec.reshape(1, -1)]
                    )

    async def update_user_taste_vector(self, telegram_id: int) -> Optional[np.ndarray]:
        """
        Пересчитывает вектор вкуса пользователя на основе всех его положительных (LIKE)
        и отрицательных (DISLIKE) взаимодействий.
        """
        async with async_session_factory() as session:
            stmt = (
                select(UserInteraction)
                .options(selectinload(UserInteraction.movie))
                .where(
                    UserInteraction.telegram_id == telegram_id,
                    UserInteraction.action.in_(["LIKE", "DISLIKE"]),
                )
                .order_by(UserInteraction.created_at.asc())
            )
            result = await session.execute(stmt)
            interactions = result.scalars().all()

            if not interactions:
                return None

            # Загружаем эмбеддинги всех фильмов одним запросом вместо N отдельных
            movie_ids = list({inter.movie_id for inter in interactions})
            emb_stmt = select(MovieEmbedding).where(MovieEmbedding.movie_id.in_(movie_ids))
            emb_res = await session.execute(emb_stmt)
            embeddings_map = {
                emb_obj.movie_id: MovieEmbedder.from_bytes(emb_obj.embedding)
                for emb_obj in emb_res.scalars().all()
            }

            pos_vectors = []
            neg_vectors = []
            genre_scores = {}

            for inter in interactions:
                vec = embeddings_map.get(inter.movie_id)
                if vec is None:
                    continue

                if inter.action == "LIKE":
                    pos_vectors.append(vec)
                    if inter.movie and inter.movie.genres:
                        for g in inter.movie.genres:
                            genre_scores[g] = genre_scores.get(g, 0) + 1
                elif inter.action == "DISLIKE":
                    neg_vectors.append(vec)
                    if inter.movie and inter.movie.genres:
                        for g in inter.movie.genres:
                            genre_scores[g] = genre_scores.get(g, 0) - 1

            if not pos_vectors:
                if neg_vectors:
                    neg_mean = np.mean(neg_vectors, axis=0)
                    taste_vec = -neg_mean
                else:
                    return None
            else:
                pos_mean = np.mean(pos_vectors, axis=0)
                if neg_vectors:
                    neg_mean = np.mean(neg_vectors, axis=0)
                    taste_vec = pos_mean - 0.35 * neg_mean
                else:
                    taste_vec = pos_mean

            norm = np.linalg.norm(taste_vec)
            if norm > 0:
                taste_vec = taste_vec / norm

            # Сохраняем в профиль пользователя
            profile_stmt = select(UserProfile).where(
                UserProfile.telegram_id == telegram_id
            )
            profile_res = await session.execute(profile_stmt)
            profile = profile_res.scalar_one_or_none()
            if profile is None:
                profile = UserProfile(
                    telegram_id=telegram_id,
                    taste_vector=MovieEmbedder.to_bytes(taste_vec),
                    preferred_genres_json=json.dumps(genre_scores, ensure_ascii=False),
                )
                session.add(profile)
            else:
                profile.taste_vector = MovieEmbedder.to_bytes(taste_vec)
                profile.preferred_genres_json = json.dumps(
                    genre_scores, ensure_ascii=False
                )

            await session.commit()
            return taste_vec

    async def get_recommendations(
        self,
        telegram_id: int,
        limit: int = 10,
        genre_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        min_rating: Optional[float] = None,
        min_year: Optional[int] = None,
    ) -> List[Movie]:
        """
        Возвращает топ персональных рекомендаций для пользователя с учетом фильтров.
        """
        await self.ensure_initialized()

        if self._embedding_matrix is None or len(self._movie_ids) == 0:
            return []

        async with async_session_factory() as session:
            # 1. Получаем профиль пользователя
            profile_stmt = select(UserProfile).where(
                UserProfile.telegram_id == telegram_id
            )
            p_res = await session.execute(profile_stmt)
            profile = p_res.scalar_one_or_none()

            taste_vector: Optional[np.ndarray] = None
            if profile and profile.taste_vector:
                taste_vector = MovieEmbedder.from_bytes(profile.taste_vector)
            else:
                # Попробуем пересчитать
                taste_vector = await self.update_user_taste_vector(telegram_id)

            # 2. Получаем ID уже просмотренных/оцененных фильмов
            inter_stmt = select(UserInteraction.movie_id).where(
                UserInteraction.telegram_id == telegram_id
            )
            inter_res = await session.execute(inter_stmt)
            excluded_ids: Set[int] = set(inter_res.scalars().all())

            # Базовый запрос
            stmt = select(Movie).where(~Movie.id.in_(excluded_ids))
            if type_filter and type_filter != "ALL":
                stmt = stmt.where(Movie.type == type_filter)
            if min_rating is not None:
                stmt = stmt.where(Movie.rating_kinopoisk >= min_rating)
            if min_year is not None:
                stmt = stmt.where(Movie.year >= min_year)

            # Если вектора вкуса нет (холодный старт), рекомендуем топ по рейтингу
            if taste_vector is None:
                stmt = stmt.order_by(Movie.rating_kinopoisk.desc().nullslast()).limit(
                    limit * 3
                )
                res = await session.execute(stmt)
                candidates = res.scalars().all()
                if genre_filter:
                    candidates = [
                        m
                        for m in candidates
                        if any(
                            genre_filter.lower() in g.lower() for g in (m.genres or [])
                        )
                    ]
                return list(candidates[:limit])

            # 3. Скоринг через матричное умножение (косинусное сходство)
            sims = self._embedding_matrix @ taste_vector  # (N,)

            res = await session.execute(stmt)
            all_available_movies = res.scalars().all()

            if genre_filter:
                all_available_movies = [
                    m
                    for m in all_available_movies
                    if any(genre_filter.lower() in g.lower() for g in (m.genres or []))
                ]

            # Сопоставляем схожесть
            id_to_idx = {mid: idx for idx, mid in enumerate(self._movie_ids)}
            scored_movies: List[Tuple[float, Movie]] = []

            preferred_genres = {}
            if profile and profile.preferred_genres_json:
                try:
                    preferred_genres = json.loads(profile.preferred_genres_json)
                except Exception:
                    pass

            for movie in all_available_movies:
                idx = id_to_idx.get(movie.id)
                if idx is None:
                    continue
                sim_score = float(sims[idx])

                genre_boost = 0.0
                if preferred_genres and movie.genres:
                    for g in movie.genres:
                        genre_boost += preferred_genres.get(g, 0) * 0.03
                genre_boost = max(-0.15, min(0.15, genre_boost))

                # Небольшая добавка за высокий рейтинг Кинопоиска
                rating_boost = 0.0
                if movie.rating_kinopoisk:
                    rating_boost = (movie.rating_kinopoisk - 6.0) * 0.03

                final_score = sim_score + genre_boost + rating_boost
                scored_movies.append((final_score, movie))

            scored_movies.sort(key=lambda x: x[0], reverse=True)
            return [m for _, m in scored_movies[:limit]]


_REC_ENGINE_INSTANCE: Optional[RecommendationEngine] = None


def get_recommendation_engine() -> RecommendationEngine:
    global _REC_ENGINE_INSTANCE
    if _REC_ENGINE_INSTANCE is None:
        _REC_ENGINE_INSTANCE = RecommendationEngine()
    return _REC_ENGINE_INSTANCE

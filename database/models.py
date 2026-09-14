import datetime
import json
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kinopoisk_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    name_ru: Mapped[str] = mapped_column(String(256), index=True)
    name_en: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    name_original: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    film_length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rating_kinopoisk: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, index=True
    )
    rating_imdb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rating_vote_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    poster_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    poster_url_preview: Mapped[Optional[str]] = mapped_column(
        String(512), nullable=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    short_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(String(32), default="FILM", index=True)
    genres_json: Mapped[str] = mapped_column(Text, default="[]")
    countries_json: Mapped[str] = mapped_column(Text, default="[]")
    web_url: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    embedding: Mapped[Optional["MovieEmbedding"]] = relationship(
        "MovieEmbedding", back_populates="movie", uselist=False, cascade="all, delete"
    )

    @property
    def genres(self) -> List[str]:
        try:
            return json.loads(self.genres_json)
        except Exception:
            return []

    @genres.setter
    def genres(self, value: List[str]):
        self.genres_json = json.dumps(value, ensure_ascii=False)

    @property
    def countries(self) -> List[str]:
        try:
            return json.loads(self.countries_json)
        except Exception:
            return []

    @countries.setter
    def countries(self, value: List[str]):
        self.countries_json = json.dumps(value, ensure_ascii=False)


class MovieEmbedding(Base):
    __tablename__ = "movie_embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.id", ondelete="CASCADE"), unique=True, index=True
    )
    embedding: Mapped[bytes] = mapped_column(LargeBinary)

    movie: Mapped["Movie"] = relationship("Movie", back_populates="embedding")


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    interactions: Mapped[List["UserInteraction"]] = relationship(
        "UserInteraction", back_populates="user", cascade="all, delete"
    )
    profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile", back_populates="user", uselist=False, cascade="all, delete"
    )


class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), index=True
    )
    movie_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.id", ondelete="CASCADE"), index=True
    )
    action: Mapped[str] = mapped_column(
        String(16), index=True
    )  # 'LIKE', 'DISLIKE', 'WATCHLIST', 'SKIP'
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="interactions")
    movie: Mapped["Movie"] = relationship("Movie")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), primary_key=True
    )
    taste_vector: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    preferred_genres_json: Mapped[str] = mapped_column(Text, default="{}")
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="profile")

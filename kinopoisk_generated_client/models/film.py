from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.film_production_status import FilmProductionStatus
from ..models.film_type import FilmType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.country import Country
  from ..models.genre import Genre





T = TypeVar("T", bound="Film")



@_attrs_define
class Film:
    """ 
        Attributes:
            kinopoisk_id (int):  Example: 301.
            kinopoisk_hd_id (None | str):  Example: 4824a95e60a7db7e86f14137516ba590.
            imdb_id (None | str):  Example: tt0133093.
            name_ru (None | str):  Example: Матрица.
            name_en (None | str):  Example: The Matrix.
            name_original (None | str):  Example: The Matrix.
            poster_url (str):  Example: https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg.
            poster_url_preview (str):  Example: https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg.
            cover_url (None | str):  Example: https://avatars.mds.yandex.net/get-
                ott/1672343/2a0000016cc7177239d4025185c488b1bf43/orig.
            logo_url (None | str):  Example: https://avatars.mds.yandex.net/get-
                ott/1648503/2a00000170a5418408119bc802b53a03007b/orig.
            reviews_count (int):  Example: 293.
            rating_good_review (float | None):  Example: 88.9.
            rating_good_review_vote_count (int | None):  Example: 257.
            rating_kinopoisk (float | None):  Example: 8.5.
            rating_kinopoisk_vote_count (int | None):  Example: 524108.
            rating_imdb (float | None):  Example: 8.7.
            rating_imdb_vote_count (int | None):  Example: 1729087.
            rating_film_critics (float | None):  Example: 7.8.
            rating_film_critics_vote_count (int | None):  Example: 155.
            rating_await (float | None):  Example: 7.8.
            rating_await_count (int | None):  Example: 2.
            rating_rf_critics (float | None):  Example: 7.8.
            rating_rf_critics_vote_count (int | None):  Example: 31.
            web_url (str):  Example: https://www.kinopoisk.ru/film/301/.
            year (int | None):  Example: 1999.
            film_length (int | None):  Example: 136.
            slogan (None | str):  Example: Добро пожаловать в реальный мир.
            description (None | str):  Example: Жизнь Томаса Андерсона разделена на две части:.
            short_description (None | str):  Example: Хакер Нео узнает, что его мир — виртуальный. Выдающийся экшен,
                доказавший, что зрелищное кино может быть умным.
            editor_annotation (None | str):  Example: Фильм доступен только на языке оригинала с русскими субтитрами.
            is_tickets_available (bool):  Example: False.
            production_status (FilmProductionStatus):  Example: POST_PRODUCTION.
            type_ (FilmType):  Example: FILM.
            rating_mpaa (None | str):  Example: r.
            rating_age_limits (None | str):  Example: age16.
            has_imax (bool | None):  Example: False.
            has_3d (bool | None):  Example: False.
            last_sync (str):  Example: 2021-07-29T20:07:49.109817.
            countries (list[Country]):
            genres (list[Genre]):
            start_year (int | None):  Example: 1996.
            end_year (int | None):  Example: 1996.
            serial (bool | None | Unset):  Example: False.
            short_film (bool | None | Unset):  Example: False.
            completed (bool | None | Unset):  Example: False.
     """

    kinopoisk_id: int
    kinopoisk_hd_id: None | str
    imdb_id: None | str
    name_ru: None | str
    name_en: None | str
    name_original: None | str
    poster_url: str
    poster_url_preview: str
    cover_url: None | str
    logo_url: None | str
    reviews_count: int
    rating_good_review: float | None
    rating_good_review_vote_count: int | None
    rating_kinopoisk: float | None
    rating_kinopoisk_vote_count: int | None
    rating_imdb: float | None
    rating_imdb_vote_count: int | None
    rating_film_critics: float | None
    rating_film_critics_vote_count: int | None
    rating_await: float | None
    rating_await_count: int | None
    rating_rf_critics: float | None
    rating_rf_critics_vote_count: int | None
    web_url: str
    year: int | None
    film_length: int | None
    slogan: None | str
    description: None | str
    short_description: None | str
    editor_annotation: None | str
    is_tickets_available: bool
    production_status: FilmProductionStatus
    type_: FilmType
    rating_mpaa: None | str
    rating_age_limits: None | str
    has_imax: bool | None
    has_3d: bool | None
    last_sync: str
    countries: list[Country]
    genres: list[Genre]
    start_year: int | None
    end_year: int | None
    serial: bool | None | Unset = UNSET
    short_film: bool | None | Unset = UNSET
    completed: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.country import Country # noqa: PLC0415
        from ..models.genre import Genre # noqa: PLC0415
        kinopoisk_id = self.kinopoisk_id

        kinopoisk_hd_id: None | str
        kinopoisk_hd_id = self.kinopoisk_hd_id

        imdb_id: None | str
        imdb_id = self.imdb_id

        name_ru: None | str
        name_ru = self.name_ru

        name_en: None | str
        name_en = self.name_en

        name_original: None | str
        name_original = self.name_original

        poster_url = self.poster_url

        poster_url_preview = self.poster_url_preview

        cover_url: None | str
        cover_url = self.cover_url

        logo_url: None | str
        logo_url = self.logo_url

        reviews_count = self.reviews_count

        rating_good_review: float | None
        rating_good_review = self.rating_good_review

        rating_good_review_vote_count: int | None
        rating_good_review_vote_count = self.rating_good_review_vote_count

        rating_kinopoisk: float | None
        rating_kinopoisk = self.rating_kinopoisk

        rating_kinopoisk_vote_count: int | None
        rating_kinopoisk_vote_count = self.rating_kinopoisk_vote_count

        rating_imdb: float | None
        rating_imdb = self.rating_imdb

        rating_imdb_vote_count: int | None
        rating_imdb_vote_count = self.rating_imdb_vote_count

        rating_film_critics: float | None
        rating_film_critics = self.rating_film_critics

        rating_film_critics_vote_count: int | None
        rating_film_critics_vote_count = self.rating_film_critics_vote_count

        rating_await: float | None
        rating_await = self.rating_await

        rating_await_count: int | None
        rating_await_count = self.rating_await_count

        rating_rf_critics: float | None
        rating_rf_critics = self.rating_rf_critics

        rating_rf_critics_vote_count: int | None
        rating_rf_critics_vote_count = self.rating_rf_critics_vote_count

        web_url = self.web_url

        year: int | None
        year = self.year

        film_length: int | None
        film_length = self.film_length

        slogan: None | str
        slogan = self.slogan

        description: None | str
        description = self.description

        short_description: None | str
        short_description = self.short_description

        editor_annotation: None | str
        editor_annotation = self.editor_annotation

        is_tickets_available = self.is_tickets_available

        production_status = self.production_status.value

        type_ = self.type_.value

        rating_mpaa: None | str
        rating_mpaa = self.rating_mpaa

        rating_age_limits: None | str
        rating_age_limits = self.rating_age_limits

        has_imax: bool | None
        has_imax = self.has_imax

        has_3d: bool | None
        has_3d = self.has_3d

        last_sync = self.last_sync

        countries = []
        for countries_item_data in self.countries:
            countries_item = countries_item_data.to_dict()
            countries.append(countries_item)



        genres = []
        for genres_item_data in self.genres:
            genres_item = genres_item_data.to_dict()
            genres.append(genres_item)



        start_year: int | None
        start_year = self.start_year

        end_year: int | None
        end_year = self.end_year

        serial: bool | None | Unset
        if isinstance(self.serial, Unset):
            serial = UNSET
        else:
            serial = self.serial

        short_film: bool | None | Unset
        if isinstance(self.short_film, Unset):
            short_film = UNSET
        else:
            short_film = self.short_film

        completed: bool | None | Unset
        if isinstance(self.completed, Unset):
            completed = UNSET
        else:
            completed = self.completed


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kinopoiskId": kinopoisk_id,
            "kinopoiskHDId": kinopoisk_hd_id,
            "imdbId": imdb_id,
            "nameRu": name_ru,
            "nameEn": name_en,
            "nameOriginal": name_original,
            "posterUrl": poster_url,
            "posterUrlPreview": poster_url_preview,
            "coverUrl": cover_url,
            "logoUrl": logo_url,
            "reviewsCount": reviews_count,
            "ratingGoodReview": rating_good_review,
            "ratingGoodReviewVoteCount": rating_good_review_vote_count,
            "ratingKinopoisk": rating_kinopoisk,
            "ratingKinopoiskVoteCount": rating_kinopoisk_vote_count,
            "ratingImdb": rating_imdb,
            "ratingImdbVoteCount": rating_imdb_vote_count,
            "ratingFilmCritics": rating_film_critics,
            "ratingFilmCriticsVoteCount": rating_film_critics_vote_count,
            "ratingAwait": rating_await,
            "ratingAwaitCount": rating_await_count,
            "ratingRfCritics": rating_rf_critics,
            "ratingRfCriticsVoteCount": rating_rf_critics_vote_count,
            "webUrl": web_url,
            "year": year,
            "filmLength": film_length,
            "slogan": slogan,
            "description": description,
            "shortDescription": short_description,
            "editorAnnotation": editor_annotation,
            "isTicketsAvailable": is_tickets_available,
            "productionStatus": production_status,
            "type": type_,
            "ratingMpaa": rating_mpaa,
            "ratingAgeLimits": rating_age_limits,
            "hasImax": has_imax,
            "has3D": has_3d,
            "lastSync": last_sync,
            "countries": countries,
            "genres": genres,
            "startYear": start_year,
            "endYear": end_year,
        })
        if serial is not UNSET:
            field_dict["serial"] = serial
        if short_film is not UNSET:
            field_dict["shortFilm"] = short_film
        if completed is not UNSET:
            field_dict["completed"] = completed

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.country import Country # noqa: PLC0415
        from ..models.genre import Genre # noqa: PLC0415
        d = dict(src_dict)
        kinopoisk_id = d.pop("kinopoiskId")

        def _parse_kinopoisk_hd_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        kinopoisk_hd_id = _parse_kinopoisk_hd_id(d.pop("kinopoiskHDId"))


        def _parse_imdb_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        imdb_id = _parse_imdb_id(d.pop("imdbId"))


        def _parse_name_ru(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name_ru = _parse_name_ru(d.pop("nameRu"))


        def _parse_name_en(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name_en = _parse_name_en(d.pop("nameEn"))


        def _parse_name_original(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name_original = _parse_name_original(d.pop("nameOriginal"))


        poster_url = d.pop("posterUrl")

        poster_url_preview = d.pop("posterUrlPreview")

        def _parse_cover_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        cover_url = _parse_cover_url(d.pop("coverUrl"))


        def _parse_logo_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        logo_url = _parse_logo_url(d.pop("logoUrl"))


        reviews_count = d.pop("reviewsCount")

        def _parse_rating_good_review(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rating_good_review = _parse_rating_good_review(d.pop("ratingGoodReview"))


        def _parse_rating_good_review_vote_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        rating_good_review_vote_count = _parse_rating_good_review_vote_count(d.pop("ratingGoodReviewVoteCount"))


        def _parse_rating_kinopoisk(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rating_kinopoisk = _parse_rating_kinopoisk(d.pop("ratingKinopoisk"))


        def _parse_rating_kinopoisk_vote_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        rating_kinopoisk_vote_count = _parse_rating_kinopoisk_vote_count(d.pop("ratingKinopoiskVoteCount"))


        def _parse_rating_imdb(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rating_imdb = _parse_rating_imdb(d.pop("ratingImdb"))


        def _parse_rating_imdb_vote_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        rating_imdb_vote_count = _parse_rating_imdb_vote_count(d.pop("ratingImdbVoteCount"))


        def _parse_rating_film_critics(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rating_film_critics = _parse_rating_film_critics(d.pop("ratingFilmCritics"))


        def _parse_rating_film_critics_vote_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        rating_film_critics_vote_count = _parse_rating_film_critics_vote_count(d.pop("ratingFilmCriticsVoteCount"))


        def _parse_rating_await(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rating_await = _parse_rating_await(d.pop("ratingAwait"))


        def _parse_rating_await_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        rating_await_count = _parse_rating_await_count(d.pop("ratingAwaitCount"))


        def _parse_rating_rf_critics(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rating_rf_critics = _parse_rating_rf_critics(d.pop("ratingRfCritics"))


        def _parse_rating_rf_critics_vote_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        rating_rf_critics_vote_count = _parse_rating_rf_critics_vote_count(d.pop("ratingRfCriticsVoteCount"))


        web_url = d.pop("webUrl")

        def _parse_year(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        year = _parse_year(d.pop("year"))


        def _parse_film_length(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        film_length = _parse_film_length(d.pop("filmLength"))


        def _parse_slogan(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        slogan = _parse_slogan(d.pop("slogan"))


        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))


        def _parse_short_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        short_description = _parse_short_description(d.pop("shortDescription"))


        def _parse_editor_annotation(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        editor_annotation = _parse_editor_annotation(d.pop("editorAnnotation"))


        is_tickets_available = d.pop("isTicketsAvailable")

        _production_status = d.pop("productionStatus", None)
        production_status: FilmProductionStatus | None
        if _production_status is None:
            production_status = None
        else:
            try:
                production_status = FilmProductionStatus(_production_status)
            except Exception:
                production_status = None

        _type = d.pop("type", None)
        type_: FilmType | None
        if _type is None:
            type_ = None
        else:
            try:
                type_ = FilmType(_type)
            except Exception:
                type_ = None




        def _parse_rating_mpaa(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rating_mpaa = _parse_rating_mpaa(d.pop("ratingMpaa"))


        def _parse_rating_age_limits(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rating_age_limits = _parse_rating_age_limits(d.pop("ratingAgeLimits"))


        def _parse_has_imax(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        has_imax = _parse_has_imax(d.pop("hasImax"))


        def _parse_has_3d(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        has_3d = _parse_has_3d(d.pop("has3D"))


        last_sync = d.pop("lastSync")

        countries = []
        _countries = d.pop("countries")
        for countries_item_data in (_countries):
            countries_item = Country.from_dict(countries_item_data)



            countries.append(countries_item)


        genres = []
        _genres = d.pop("genres")
        for genres_item_data in (_genres):
            genres_item = Genre.from_dict(genres_item_data)



            genres.append(genres_item)


        def _parse_start_year(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        start_year = _parse_start_year(d.pop("startYear"))


        def _parse_end_year(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        end_year = _parse_end_year(d.pop("endYear"))


        def _parse_serial(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        serial = _parse_serial(d.pop("serial", UNSET))


        def _parse_short_film(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        short_film = _parse_short_film(d.pop("shortFilm", UNSET))


        def _parse_completed(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        completed = _parse_completed(d.pop("completed", UNSET))


        film = cls(
            kinopoisk_id=kinopoisk_id,
            kinopoisk_hd_id=kinopoisk_hd_id,
            imdb_id=imdb_id,
            name_ru=name_ru,
            name_en=name_en,
            name_original=name_original,
            poster_url=poster_url,
            poster_url_preview=poster_url_preview,
            cover_url=cover_url,
            logo_url=logo_url,
            reviews_count=reviews_count,
            rating_good_review=rating_good_review,
            rating_good_review_vote_count=rating_good_review_vote_count,
            rating_kinopoisk=rating_kinopoisk,
            rating_kinopoisk_vote_count=rating_kinopoisk_vote_count,
            rating_imdb=rating_imdb,
            rating_imdb_vote_count=rating_imdb_vote_count,
            rating_film_critics=rating_film_critics,
            rating_film_critics_vote_count=rating_film_critics_vote_count,
            rating_await=rating_await,
            rating_await_count=rating_await_count,
            rating_rf_critics=rating_rf_critics,
            rating_rf_critics_vote_count=rating_rf_critics_vote_count,
            web_url=web_url,
            year=year,
            film_length=film_length,
            slogan=slogan,
            description=description,
            short_description=short_description,
            editor_annotation=editor_annotation,
            is_tickets_available=is_tickets_available,
            production_status=production_status,
            type_=type_,
            rating_mpaa=rating_mpaa,
            rating_age_limits=rating_age_limits,
            has_imax=has_imax,
            has_3d=has_3d,
            last_sync=last_sync,
            countries=countries,
            genres=genres,
            start_year=start_year,
            end_year=end_year,
            serial=serial,
            short_film=short_film,
            completed=completed,
        )


        film.additional_properties = d
        return film

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

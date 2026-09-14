from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.film_search_by_filters_response_items_type import FilmSearchByFiltersResponseItemsType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.country import Country
  from ..models.genre import Genre





T = TypeVar("T", bound="FilmSearchByFiltersResponseItems")



@_attrs_define
class FilmSearchByFiltersResponseItems:
    """ 
        Attributes:
            kinopoisk_id (int | Unset):  Example: 263531.
            imdb_id (None | str | Unset):  Example: tt0050561.
            name_ru (None | str | Unset):  Example: Мстители.
            name_en (None | str | Unset):  Example: The Avengers.
            name_original (None | str | Unset):  Example: The Avengers.
            countries (list[Country] | Unset):
            genres (list[Genre] | Unset):
            rating_kinopoisk (float | None | Unset):  Example: 7.9.
            rating_imdb (float | None | Unset):  Example: 7.9.
            year (float | None | Unset):  Example: 2012.
            type_ (FilmSearchByFiltersResponseItemsType | Unset):  Example: FILM.
            poster_url (str | Unset):  Example: http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg.
            poster_url_preview (str | Unset):  Example: https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg.
     """

    kinopoisk_id: int | Unset = UNSET
    imdb_id: None | str | Unset = UNSET
    name_ru: None | str | Unset = UNSET
    name_en: None | str | Unset = UNSET
    name_original: None | str | Unset = UNSET
    countries: list[Country] | Unset = UNSET
    genres: list[Genre] | Unset = UNSET
    rating_kinopoisk: float | None | Unset = UNSET
    rating_imdb: float | None | Unset = UNSET
    year: float | None | Unset = UNSET
    type_: FilmSearchByFiltersResponseItemsType | Unset = UNSET
    poster_url: str | Unset = UNSET
    poster_url_preview: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.country import Country # noqa: PLC0415
        from ..models.genre import Genre # noqa: PLC0415
        kinopoisk_id = self.kinopoisk_id

        imdb_id: None | str | Unset
        if isinstance(self.imdb_id, Unset):
            imdb_id = UNSET
        else:
            imdb_id = self.imdb_id

        name_ru: None | str | Unset
        if isinstance(self.name_ru, Unset):
            name_ru = UNSET
        else:
            name_ru = self.name_ru

        name_en: None | str | Unset
        if isinstance(self.name_en, Unset):
            name_en = UNSET
        else:
            name_en = self.name_en

        name_original: None | str | Unset
        if isinstance(self.name_original, Unset):
            name_original = UNSET
        else:
            name_original = self.name_original

        countries: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.countries, Unset):
            countries = []
            for countries_item_data in self.countries:
                countries_item = countries_item_data.to_dict()
                countries.append(countries_item)



        genres: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.genres, Unset):
            genres = []
            for genres_item_data in self.genres:
                genres_item = genres_item_data.to_dict()
                genres.append(genres_item)



        rating_kinopoisk: float | None | Unset
        if isinstance(self.rating_kinopoisk, Unset):
            rating_kinopoisk = UNSET
        else:
            rating_kinopoisk = self.rating_kinopoisk

        rating_imdb: float | None | Unset
        if isinstance(self.rating_imdb, Unset):
            rating_imdb = UNSET
        else:
            rating_imdb = self.rating_imdb

        year: float | None | Unset
        if isinstance(self.year, Unset):
            year = UNSET
        else:
            year = self.year

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        poster_url = self.poster_url

        poster_url_preview = self.poster_url_preview


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if kinopoisk_id is not UNSET:
            field_dict["kinopoiskId"] = kinopoisk_id
        if imdb_id is not UNSET:
            field_dict["imdbId"] = imdb_id
        if name_ru is not UNSET:
            field_dict["nameRu"] = name_ru
        if name_en is not UNSET:
            field_dict["nameEn"] = name_en
        if name_original is not UNSET:
            field_dict["nameOriginal"] = name_original
        if countries is not UNSET:
            field_dict["countries"] = countries
        if genres is not UNSET:
            field_dict["genres"] = genres
        if rating_kinopoisk is not UNSET:
            field_dict["ratingKinopoisk"] = rating_kinopoisk
        if rating_imdb is not UNSET:
            field_dict["ratingImdb"] = rating_imdb
        if year is not UNSET:
            field_dict["year"] = year
        if type_ is not UNSET:
            field_dict["type"] = type_
        if poster_url is not UNSET:
            field_dict["posterUrl"] = poster_url
        if poster_url_preview is not UNSET:
            field_dict["posterUrlPreview"] = poster_url_preview

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.country import Country # noqa: PLC0415
        from ..models.genre import Genre # noqa: PLC0415
        d = dict(src_dict)
        kinopoisk_id = d.pop("kinopoiskId", UNSET)

        def _parse_imdb_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        imdb_id = _parse_imdb_id(d.pop("imdbId", UNSET))


        def _parse_name_ru(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name_ru = _parse_name_ru(d.pop("nameRu", UNSET))


        def _parse_name_en(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name_en = _parse_name_en(d.pop("nameEn", UNSET))


        def _parse_name_original(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name_original = _parse_name_original(d.pop("nameOriginal", UNSET))


        _countries = d.pop("countries", UNSET)
        countries: list[Country] | Unset = UNSET
        if _countries is not UNSET:
            countries = []
            for countries_item_data in _countries:
                countries_item = Country.from_dict(countries_item_data)



                countries.append(countries_item)


        _genres = d.pop("genres", UNSET)
        genres: list[Genre] | Unset = UNSET
        if _genres is not UNSET:
            genres = []
            for genres_item_data in _genres:
                genres_item = Genre.from_dict(genres_item_data)



                genres.append(genres_item)


        def _parse_rating_kinopoisk(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        rating_kinopoisk = _parse_rating_kinopoisk(d.pop("ratingKinopoisk", UNSET))


        def _parse_rating_imdb(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        rating_imdb = _parse_rating_imdb(d.pop("ratingImdb", UNSET))


        def _parse_year(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        year = _parse_year(d.pop("year", UNSET))


        _type_ = d.pop("type", UNSET)
        type_: FilmSearchByFiltersResponseItemsType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = FilmSearchByFiltersResponseItemsType(_type_)




        poster_url = d.pop("posterUrl", UNSET)

        poster_url_preview = d.pop("posterUrlPreview", UNSET)

        film_search_by_filters_response_items = cls(
            kinopoisk_id=kinopoisk_id,
            imdb_id=imdb_id,
            name_ru=name_ru,
            name_en=name_en,
            name_original=name_original,
            countries=countries,
            genres=genres,
            rating_kinopoisk=rating_kinopoisk,
            rating_imdb=rating_imdb,
            year=year,
            type_=type_,
            poster_url=poster_url,
            poster_url_preview=poster_url_preview,
        )


        film_search_by_filters_response_items.additional_properties = d
        return film_search_by_filters_response_items

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

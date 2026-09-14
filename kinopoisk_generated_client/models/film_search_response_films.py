from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.film_search_response_films_type import FilmSearchResponseFilmsType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.country import Country
  from ..models.genre import Genre





T = TypeVar("T", bound="FilmSearchResponseFilms")



@_attrs_define
class FilmSearchResponseFilms:
    """ 
        Attributes:
            film_id (int | Unset):  Example: 263531.
            name_ru (str | Unset):  Example: Мстители.
            name_en (str | Unset):  Example: The Avengers.
            type_ (FilmSearchResponseFilmsType | Unset):  Example: FILM.
            year (str | Unset):  Example: 2012.
            description (str | Unset):  Example: США, Джосс Уидон(фантастика).
            film_length (str | Unset):  Example: 2:17.
            countries (list[Country] | Unset):
            genres (list[Genre] | Unset):
            rating (str | Unset):  Example: NOTE!!! 7.9 for released film or 99% if film have not released yet.
            rating_vote_count (int | Unset):  Example: 284245.
            poster_url (str | Unset):  Example: http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg.
            poster_url_preview (str | Unset):  Example: https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg.
     """

    film_id: int | Unset = UNSET
    name_ru: str | Unset = UNSET
    name_en: str | Unset = UNSET
    type_: FilmSearchResponseFilmsType | Unset = UNSET
    year: str | Unset = UNSET
    description: str | Unset = UNSET
    film_length: str | Unset = UNSET
    countries: list[Country] | Unset = UNSET
    genres: list[Genre] | Unset = UNSET
    rating: str | Unset = UNSET
    rating_vote_count: int | Unset = UNSET
    poster_url: str | Unset = UNSET
    poster_url_preview: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.country import Country # noqa: PLC0415
        from ..models.genre import Genre # noqa: PLC0415
        film_id = self.film_id

        name_ru = self.name_ru

        name_en = self.name_en

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        year = self.year

        description = self.description

        film_length = self.film_length

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



        rating = self.rating

        rating_vote_count = self.rating_vote_count

        poster_url = self.poster_url

        poster_url_preview = self.poster_url_preview


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if film_id is not UNSET:
            field_dict["filmId"] = film_id
        if name_ru is not UNSET:
            field_dict["nameRu"] = name_ru
        if name_en is not UNSET:
            field_dict["nameEn"] = name_en
        if type_ is not UNSET:
            field_dict["type"] = type_
        if year is not UNSET:
            field_dict["year"] = year
        if description is not UNSET:
            field_dict["description"] = description
        if film_length is not UNSET:
            field_dict["filmLength"] = film_length
        if countries is not UNSET:
            field_dict["countries"] = countries
        if genres is not UNSET:
            field_dict["genres"] = genres
        if rating is not UNSET:
            field_dict["rating"] = rating
        if rating_vote_count is not UNSET:
            field_dict["ratingVoteCount"] = rating_vote_count
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
        film_id = d.pop("filmId", UNSET)

        name_ru = d.pop("nameRu", UNSET)

        name_en = d.pop("nameEn", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: FilmSearchResponseFilmsType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = FilmSearchResponseFilmsType(_type_)




        year = d.pop("year", UNSET)

        description = d.pop("description", UNSET)

        film_length = d.pop("filmLength", UNSET)

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


        rating = d.pop("rating", UNSET)

        rating_vote_count = d.pop("ratingVoteCount", UNSET)

        poster_url = d.pop("posterUrl", UNSET)

        poster_url_preview = d.pop("posterUrlPreview", UNSET)

        film_search_response_films = cls(
            film_id=film_id,
            name_ru=name_ru,
            name_en=name_en,
            type_=type_,
            year=year,
            description=description,
            film_length=film_length,
            countries=countries,
            genres=genres,
            rating=rating,
            rating_vote_count=rating_vote_count,
            poster_url=poster_url,
            poster_url_preview=poster_url_preview,
        )


        film_search_response_films.additional_properties = d
        return film_search_response_films

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

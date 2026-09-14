from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.person_response_films_profession_key import PersonResponseFilmsProfessionKey
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="PersonResponseFilms")



@_attrs_define
class PersonResponseFilms:
    """ 
        Attributes:
            film_id (int | Unset):  Example: 32169.
            name_ru (None | str | Unset):  Example: Солист.
            name_en (None | str | Unset):  Example: The Soloist.
            rating (None | str | Unset):  Example: 7.2 or 76% if film has not released yet.
            year (None | str | Unset):  Example: 2009.
            general (bool | Unset):  Example: False.
            description (None | str | Unset):  Example: Steve Lopez.
            profession_key (PersonResponseFilmsProfessionKey | Unset):  Example: ACTOR.
     """

    film_id: int | Unset = UNSET
    name_ru: None | str | Unset = UNSET
    name_en: None | str | Unset = UNSET
    rating: None | str | Unset = UNSET
    year: None | str | Unset = UNSET
    general: bool | Unset = UNSET
    description: None | str | Unset = UNSET
    profession_key: PersonResponseFilmsProfessionKey | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        film_id = self.film_id

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

        rating: None | str | Unset
        if isinstance(self.rating, Unset):
            rating = UNSET
        else:
            rating = self.rating

        year: None | str | Unset
        if isinstance(self.year, Unset):
            year = UNSET
        else:
            year = self.year

        general = self.general

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        profession_key: str | Unset = UNSET
        if not isinstance(self.profession_key, Unset):
            profession_key = self.profession_key.value



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
        if rating is not UNSET:
            field_dict["rating"] = rating
        if year is not UNSET:
            field_dict["year"] = year
        if general is not UNSET:
            field_dict["general"] = general
        if description is not UNSET:
            field_dict["description"] = description
        if profession_key is not UNSET:
            field_dict["professionKey"] = profession_key

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        film_id = d.pop("filmId", UNSET)

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


        def _parse_rating(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rating = _parse_rating(d.pop("rating", UNSET))


        def _parse_year(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        year = _parse_year(d.pop("year", UNSET))


        general = d.pop("general", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        _profession_key = d.pop("professionKey", UNSET)
        profession_key: PersonResponseFilmsProfessionKey | Unset
        if isinstance(_profession_key,  Unset):
            profession_key = UNSET
        else:
            profession_key = PersonResponseFilmsProfessionKey(_profession_key)




        person_response_films = cls(
            film_id=film_id,
            name_ru=name_ru,
            name_en=name_en,
            rating=rating,
            year=year,
            general=general,
            description=description,
            profession_key=profession_key,
        )


        person_response_films.additional_properties = d
        return person_response_films

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

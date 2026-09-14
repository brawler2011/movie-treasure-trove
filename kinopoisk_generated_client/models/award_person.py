from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="AwardPerson")



@_attrs_define
class AwardPerson:
    """ 
        Attributes:
            kinopoisk_id (int):  Example: 1937039.
            web_url (str):  Example: https://www.kinopoisk.ru/name/1937039/.
            name_ru (None | str):  Example: Джон Т. Рейц.
            name_en (None | str):  Example: John T. Reitz.
            sex (str):  Example: MALE.
            poster_url (str):  Example: https://kinopoiskapiunofficial.tech/images/actor_posters/kp/1937039.jpg.
            growth (int | None):  Example: 178.
            birthday (None | str):  Example: 1955-11-02.
            death (None | str):  Example: 2019-01-06.
            age (int | None):  Example: 21.
            birthplace (None | str):  Example: Лос-Анджелес, Калифорния, США.
            deathplace (None | str):  Example: Лос-Анджелес, Калифорния, США.
            profession (None | str):  Example: Монтажер, Продюсер.
     """

    kinopoisk_id: int
    web_url: str
    name_ru: None | str
    name_en: None | str
    sex: str
    poster_url: str
    growth: int | None
    birthday: None | str
    death: None | str
    age: int | None
    birthplace: None | str
    deathplace: None | str
    profession: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kinopoisk_id = self.kinopoisk_id

        web_url = self.web_url

        name_ru: None | str
        name_ru = self.name_ru

        name_en: None | str
        name_en = self.name_en

        sex = self.sex

        poster_url = self.poster_url

        growth: int | None
        growth = self.growth

        birthday: None | str
        birthday = self.birthday

        death: None | str
        death = self.death

        age: int | None
        age = self.age

        birthplace: None | str
        birthplace = self.birthplace

        deathplace: None | str
        deathplace = self.deathplace

        profession: None | str
        profession = self.profession


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kinopoiskId": kinopoisk_id,
            "webUrl": web_url,
            "nameRu": name_ru,
            "nameEn": name_en,
            "sex": sex,
            "posterUrl": poster_url,
            "growth": growth,
            "birthday": birthday,
            "death": death,
            "age": age,
            "birthplace": birthplace,
            "deathplace": deathplace,
            "profession": profession,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kinopoisk_id = d.pop("kinopoiskId")

        web_url = d.pop("webUrl")

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


        sex = d.pop("sex")

        poster_url = d.pop("posterUrl")

        def _parse_growth(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        growth = _parse_growth(d.pop("growth"))


        def _parse_birthday(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        birthday = _parse_birthday(d.pop("birthday"))


        def _parse_death(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        death = _parse_death(d.pop("death"))


        def _parse_age(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        age = _parse_age(d.pop("age"))


        def _parse_birthplace(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        birthplace = _parse_birthplace(d.pop("birthplace"))


        def _parse_deathplace(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        deathplace = _parse_deathplace(d.pop("deathplace"))


        def _parse_profession(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        profession = _parse_profession(d.pop("profession"))


        award_person = cls(
            kinopoisk_id=kinopoisk_id,
            web_url=web_url,
            name_ru=name_ru,
            name_en=name_en,
            sex=sex,
            poster_url=poster_url,
            growth=growth,
            birthday=birthday,
            death=death,
            age=age,
            birthplace=birthplace,
            deathplace=deathplace,
            profession=profession,
        )


        award_person.additional_properties = d
        return award_person

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

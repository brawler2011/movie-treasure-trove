from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.person_response_sex import PersonResponseSex
from typing import cast

if TYPE_CHECKING:
  from ..models.person_response_films import PersonResponseFilms
  from ..models.person_response_spouses import PersonResponseSpouses





T = TypeVar("T", bound="PersonResponse")



@_attrs_define
class PersonResponse:
    """ 
        Attributes:
            person_id (int):  Example: 66539.
            web_url (None | str):  Example: 10096.
            name_ru (None | str):  Example: Винс Гиллиган.
            name_en (None | str):  Example: Vince Gilligan.
            sex (PersonResponseSex):  Example: MALE.
            poster_url (str):  Example: https://kinopoiskapiunofficial.tech/images/actor_posters/kp/10096.jpg.
            growth (None | str):  Example: 174.
            birthday (None | str):  Example: 1965-04-04.
            death (None | str):  Example: 2008-01-22.
            age (int | None):  Example: 55.
            birthplace (None | str):  Example: Манхэттэн, Нью-Йорк, США.
            deathplace (None | str):  Example: Манхэттэн, Нью-Йорк, США.
            has_awards (int | None):  Example: 1.
            profession (None | str):  Example: Актер, Продюсер, Сценарист.
            facts (list[str]):
            spouses (list[PersonResponseSpouses]):
            films (list[PersonResponseFilms]):
     """

    person_id: int
    web_url: None | str
    name_ru: None | str
    name_en: None | str
    sex: PersonResponseSex
    poster_url: str
    growth: None | str
    birthday: None | str
    death: None | str
    age: int | None
    birthplace: None | str
    deathplace: None | str
    has_awards: int | None
    profession: None | str
    facts: list[str]
    spouses: list[PersonResponseSpouses]
    films: list[PersonResponseFilms]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.person_response_films import PersonResponseFilms # noqa: PLC0415
        from ..models.person_response_spouses import PersonResponseSpouses # noqa: PLC0415
        person_id = self.person_id

        web_url: None | str
        web_url = self.web_url

        name_ru: None | str
        name_ru = self.name_ru

        name_en: None | str
        name_en = self.name_en

        sex = self.sex.value

        poster_url = self.poster_url

        growth: None | str
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

        has_awards: int | None
        has_awards = self.has_awards

        profession: None | str
        profession = self.profession

        facts = self.facts



        spouses = []
        for spouses_item_data in self.spouses:
            spouses_item = spouses_item_data.to_dict()
            spouses.append(spouses_item)



        films = []
        for films_item_data in self.films:
            films_item = films_item_data.to_dict()
            films.append(films_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "personId": person_id,
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
            "hasAwards": has_awards,
            "profession": profession,
            "facts": facts,
            "spouses": spouses,
            "films": films,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.person_response_films import PersonResponseFilms # noqa: PLC0415
        from ..models.person_response_spouses import PersonResponseSpouses # noqa: PLC0415
        d = dict(src_dict)
        person_id = d.pop("personId")

        def _parse_web_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        web_url = _parse_web_url(d.pop("webUrl"))


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


        sex = PersonResponseSex(d.pop("sex"))




        poster_url = d.pop("posterUrl")

        def _parse_growth(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

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


        def _parse_has_awards(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        has_awards = _parse_has_awards(d.pop("hasAwards"))


        def _parse_profession(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        profession = _parse_profession(d.pop("profession"))


        facts = cast(list[str], d.pop("facts"))


        spouses = []
        _spouses = d.pop("spouses")
        for spouses_item_data in (_spouses):
            spouses_item = PersonResponseSpouses.from_dict(spouses_item_data)



            spouses.append(spouses_item)


        films = []
        _films = d.pop("films")
        for films_item_data in (_films):
            films_item = PersonResponseFilms.from_dict(films_item_data)



            films.append(films_item)


        person_response = cls(
            person_id=person_id,
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
            has_awards=has_awards,
            profession=profession,
            facts=facts,
            spouses=spouses,
            films=films,
        )


        person_response.additional_properties = d
        return person_response

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

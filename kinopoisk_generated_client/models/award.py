from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.award_person import AwardPerson





T = TypeVar("T", bound="Award")



@_attrs_define
class Award:
    """ 
        Attributes:
            name (str):  Example: Оскар.
            win (bool):  Example: True.
            image_url (None | str):  Example: https://avatars.mds.yandex.net/get-kinopoisk-
                image/1600647/09035193-2458-4de7-a7df-ad8f85b73798/orig.
            nomination_name (str):  Example: Лучший звук.
            year (int):  Example: 2000.
            persons (list[AwardPerson] | Unset):
     """

    name: str
    win: bool
    image_url: None | str
    nomination_name: str
    year: int
    persons: list[AwardPerson] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.award_person import AwardPerson # noqa: PLC0415
        name = self.name

        win = self.win

        image_url: None | str
        image_url = self.image_url

        nomination_name = self.nomination_name

        year = self.year

        persons: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.persons, Unset):
            persons = []
            for persons_item_data in self.persons:
                persons_item = persons_item_data.to_dict()
                persons.append(persons_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "win": win,
            "imageUrl": image_url,
            "nominationName": nomination_name,
            "year": year,
        })
        if persons is not UNSET:
            field_dict["persons"] = persons

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.award_person import AwardPerson # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        win = d.pop("win")

        def _parse_image_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        image_url = _parse_image_url(d.pop("imageUrl"))


        nomination_name = d.pop("nominationName")

        year = d.pop("year")

        _persons = d.pop("persons", UNSET)
        persons: list[AwardPerson] | Unset = UNSET
        if _persons is not UNSET:
            persons = []
            for persons_item_data in _persons:
                persons_item = AwardPerson.from_dict(persons_item_data)



                persons.append(persons_item)


        award = cls(
            name=name,
            win=win,
            image_url=image_url,
            nomination_name=nomination_name,
            year=year,
            persons=persons,
        )


        award.additional_properties = d
        return award

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

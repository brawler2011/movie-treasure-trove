from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.person_response_spouses_sex import PersonResponseSpousesSex
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="PersonResponseSpouses")



@_attrs_define
class PersonResponseSpouses:
    """ 
        Attributes:
            person_id (int | Unset):  Example: 32169.
            name (None | str | Unset):  Example: Сьюзан Дауни.
            divorced (bool | Unset):  Example: False.
            divorced_reason (None | str | Unset):
            sex (PersonResponseSpousesSex | Unset):  Example: MALE.
            children (int | Unset):  Example: 2.
            web_url (str | Unset):  Example: https://www.kinopoisk.ru/name/32169/.
            relation (str | Unset):  Example: супруга.
     """

    person_id: int | Unset = UNSET
    name: None | str | Unset = UNSET
    divorced: bool | Unset = UNSET
    divorced_reason: None | str | Unset = UNSET
    sex: PersonResponseSpousesSex | Unset = UNSET
    children: int | Unset = UNSET
    web_url: str | Unset = UNSET
    relation: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        person_id = self.person_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        divorced = self.divorced

        divorced_reason: None | str | Unset
        if isinstance(self.divorced_reason, Unset):
            divorced_reason = UNSET
        else:
            divorced_reason = self.divorced_reason

        sex: str | Unset = UNSET
        if not isinstance(self.sex, Unset):
            sex = self.sex.value


        children = self.children

        web_url = self.web_url

        relation = self.relation


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if person_id is not UNSET:
            field_dict["personId"] = person_id
        if name is not UNSET:
            field_dict["name"] = name
        if divorced is not UNSET:
            field_dict["divorced"] = divorced
        if divorced_reason is not UNSET:
            field_dict["divorcedReason"] = divorced_reason
        if sex is not UNSET:
            field_dict["sex"] = sex
        if children is not UNSET:
            field_dict["children"] = children
        if web_url is not UNSET:
            field_dict["webUrl"] = web_url
        if relation is not UNSET:
            field_dict["relation"] = relation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        person_id = d.pop("personId", UNSET)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))


        divorced = d.pop("divorced", UNSET)

        def _parse_divorced_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        divorced_reason = _parse_divorced_reason(d.pop("divorcedReason", UNSET))


        _sex = d.pop("sex", UNSET)
        sex: PersonResponseSpousesSex | Unset
        if isinstance(_sex,  Unset):
            sex = UNSET
        else:
            sex = PersonResponseSpousesSex(_sex)




        children = d.pop("children", UNSET)

        web_url = d.pop("webUrl", UNSET)

        relation = d.pop("relation", UNSET)

        person_response_spouses = cls(
            person_id=person_id,
            name=name,
            divorced=divorced,
            divorced_reason=divorced_reason,
            sex=sex,
            children=children,
            web_url=web_url,
            relation=relation,
        )


        person_response_spouses.additional_properties = d
        return person_response_spouses

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

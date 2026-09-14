from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.fact_type import FactType






T = TypeVar("T", bound="Fact")



@_attrs_define
class Fact:
    """ 
        Attributes:
            text (str):  Example: В эпизоде, где Тринити и Нео в поисках Морфиуса оказываются на крыше....
            type_ (FactType):  Example: BLOOPER.
            spoiler (bool):  Example: False.
     """

    text: str
    type_: FactType
    spoiler: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        text = self.text

        type_ = self.type_.value

        spoiler = self.spoiler


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "text": text,
            "type": type_,
            "spoiler": spoiler,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        text = d.pop("text")

        type_ = FactType(d.pop("type"))




        spoiler = d.pop("spoiler")

        fact = cls(
            text=text,
            type_=type_,
            spoiler=spoiler,
        )


        fact.additional_properties = d
        return fact

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

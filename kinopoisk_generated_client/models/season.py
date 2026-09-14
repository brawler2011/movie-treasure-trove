from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.episode import Episode





T = TypeVar("T", bound="Season")



@_attrs_define
class Season:
    """ 
        Attributes:
            number (int):  Example: 1.
            episodes (list[Episode]):
     """

    number: int
    episodes: list[Episode]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.episode import Episode # noqa: PLC0415
        number = self.number

        episodes = []
        for episodes_item_data in self.episodes:
            episodes_item = episodes_item_data.to_dict()
            episodes.append(episodes_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "number": number,
            "episodes": episodes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.episode import Episode # noqa: PLC0415
        d = dict(src_dict)
        number = d.pop("number")

        episodes = []
        _episodes = d.pop("episodes")
        for episodes_item_data in (_episodes):
            episodes_item = Episode.from_dict(episodes_item_data)



            episodes.append(episodes_item)


        season = cls(
            number=number,
            episodes=episodes,
        )


        season.additional_properties = d
        return season

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

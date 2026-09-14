from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.digital_release_item import DigitalReleaseItem





T = TypeVar("T", bound="DigitalReleaseResponse")



@_attrs_define
class DigitalReleaseResponse:
    """ 
        Attributes:
            page (int):  Example: 1.
            total (int):  Example: 34.
            releases (list[DigitalReleaseItem]):
     """

    page: int
    total: int
    releases: list[DigitalReleaseItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.digital_release_item import DigitalReleaseItem # noqa: PLC0415
        page = self.page

        total = self.total

        releases = []
        for releases_item_data in self.releases:
            releases_item = releases_item_data.to_dict()
            releases.append(releases_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "page": page,
            "total": total,
            "releases": releases,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.digital_release_item import DigitalReleaseItem # noqa: PLC0415
        d = dict(src_dict)
        page = d.pop("page")

        total = d.pop("total")

        releases = []
        _releases = d.pop("releases")
        for releases_item_data in (_releases):
            releases_item = DigitalReleaseItem.from_dict(releases_item_data)



            releases.append(releases_item)


        digital_release_response = cls(
            page=page,
            total=total,
            releases=releases,
        )


        digital_release_response.additional_properties = d
        return digital_release_response

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

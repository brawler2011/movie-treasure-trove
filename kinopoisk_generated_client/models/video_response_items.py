from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.video_response_items_site import VideoResponseItemsSite
from ..types import UNSET, Unset






T = TypeVar("T", bound="VideoResponseItems")



@_attrs_define
class VideoResponseItems:
    """ 
        Attributes:
            url (str | Unset):  Example: https://www.youtube.com/watch?v=gbcVZgO4n4E.
            name (str | Unset):  Example: Мстители: Финал – официальный трейлер (16+).
            site (VideoResponseItemsSite | Unset):  Example: YOUTUBE.
     """

    url: str | Unset = UNSET
    name: str | Unset = UNSET
    site: VideoResponseItemsSite | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        url = self.url

        name = self.name

        site: str | Unset = UNSET
        if not isinstance(self.site, Unset):
            site = self.site.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if url is not UNSET:
            field_dict["url"] = url
        if name is not UNSET:
            field_dict["name"] = name
        if site is not UNSET:
            field_dict["site"] = site

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        name = d.pop("name", UNSET)

        _site = d.pop("site", UNSET)
        site: VideoResponseItemsSite | Unset
        if isinstance(_site,  Unset):
            site = UNSET
        else:
            site = VideoResponseItemsSite(_site)




        video_response_items = cls(
            url=url,
            name=name,
            site=site,
        )


        video_response_items.additional_properties = d
        return video_response_items

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

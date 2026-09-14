from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="Episode")



@_attrs_define
class Episode:
    """ 
        Attributes:
            season_number (int):  Example: 1.
            episode_number (int):  Example: 1.
            name_ru (None | str):
            name_en (None | str):  Example: Chapter One: The Vanishing of Will Byers.
            synopsis (None | str):  Example: The Vanishing of Will Byers....
            release_date (None | str):  Example: 2016-07-15.
     """

    season_number: int
    episode_number: int
    name_ru: None | str
    name_en: None | str
    synopsis: None | str
    release_date: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        season_number = self.season_number

        episode_number = self.episode_number

        name_ru: None | str
        name_ru = self.name_ru

        name_en: None | str
        name_en = self.name_en

        synopsis: None | str
        synopsis = self.synopsis

        release_date: None | str
        release_date = self.release_date


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "seasonNumber": season_number,
            "episodeNumber": episode_number,
            "nameRu": name_ru,
            "nameEn": name_en,
            "synopsis": synopsis,
            "releaseDate": release_date,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        season_number = d.pop("seasonNumber")

        episode_number = d.pop("episodeNumber")

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


        def _parse_synopsis(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        synopsis = _parse_synopsis(d.pop("synopsis"))


        def _parse_release_date(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        release_date = _parse_release_date(d.pop("releaseDate"))


        episode = cls(
            season_number=season_number,
            episode_number=episode_number,
            name_ru=name_ru,
            name_en=name_en,
            synopsis=synopsis,
            release_date=release_date,
        )


        episode.additional_properties = d
        return episode

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

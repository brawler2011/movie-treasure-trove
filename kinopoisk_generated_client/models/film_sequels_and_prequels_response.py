from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.film_sequels_and_prequels_response_relation_type import FilmSequelsAndPrequelsResponseRelationType






T = TypeVar("T", bound="FilmSequelsAndPrequelsResponse")



@_attrs_define
class FilmSequelsAndPrequelsResponse:
    """ 
        Attributes:
            film_id (int):  Example: 301.
            name_ru (str):  Example: Матрица.
            name_en (str):  Example: The Matrix.
            name_original (str):  Example: The Matrix.
            poster_url (str):  Example: https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg.
            poster_url_preview (str):  Example: https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg.
            relation_type (FilmSequelsAndPrequelsResponseRelationType):  Example: SEQUEL.
     """

    film_id: int
    name_ru: str
    name_en: str
    name_original: str
    poster_url: str
    poster_url_preview: str
    relation_type: FilmSequelsAndPrequelsResponseRelationType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        film_id = self.film_id

        name_ru = self.name_ru

        name_en = self.name_en

        name_original = self.name_original

        poster_url = self.poster_url

        poster_url_preview = self.poster_url_preview

        relation_type = self.relation_type.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "filmId": film_id,
            "nameRu": name_ru,
            "nameEn": name_en,
            "nameOriginal": name_original,
            "posterUrl": poster_url,
            "posterUrlPreview": poster_url_preview,
            "relationType": relation_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        film_id = d.pop("filmId")

        name_ru = d.pop("nameRu")

        name_en = d.pop("nameEn")

        name_original = d.pop("nameOriginal")

        poster_url = d.pop("posterUrl")

        poster_url_preview = d.pop("posterUrlPreview")

        relation_type = FilmSequelsAndPrequelsResponseRelationType(d.pop("relationType"))




        film_sequels_and_prequels_response = cls(
            film_id=film_id,
            name_ru=name_ru,
            name_en=name_en,
            name_original=name_original,
            poster_url=poster_url,
            poster_url_preview=poster_url_preview,
            relation_type=relation_type,
        )


        film_sequels_and_prequels_response.additional_properties = d
        return film_sequels_and_prequels_response

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

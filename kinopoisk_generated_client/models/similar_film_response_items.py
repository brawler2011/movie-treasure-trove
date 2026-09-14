from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.similar_film_response_items_relation_type import SimilarFilmResponseItemsRelationType
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SimilarFilmResponseItems")



@_attrs_define
class SimilarFilmResponseItems:
    """ 
        Attributes:
            film_id (int | Unset):  Example: 301.
            name_ru (None | str | Unset):  Example: Матрица.
            name_en (None | str | Unset):  Example: The Matrix.
            name_original (None | str | Unset):  Example: The Matrix.
            poster_url (str | Unset):  Example: https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg.
            poster_url_preview (str | Unset):  Example: https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg.
            relation_type (SimilarFilmResponseItemsRelationType | Unset):  Example: SIMILAR.
     """

    film_id: int | Unset = UNSET
    name_ru: None | str | Unset = UNSET
    name_en: None | str | Unset = UNSET
    name_original: None | str | Unset = UNSET
    poster_url: str | Unset = UNSET
    poster_url_preview: str | Unset = UNSET
    relation_type: SimilarFilmResponseItemsRelationType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        film_id = self.film_id

        name_ru: None | str | Unset
        if isinstance(self.name_ru, Unset):
            name_ru = UNSET
        else:
            name_ru = self.name_ru

        name_en: None | str | Unset
        if isinstance(self.name_en, Unset):
            name_en = UNSET
        else:
            name_en = self.name_en

        name_original: None | str | Unset
        if isinstance(self.name_original, Unset):
            name_original = UNSET
        else:
            name_original = self.name_original

        poster_url = self.poster_url

        poster_url_preview = self.poster_url_preview

        relation_type: str | Unset = UNSET
        if not isinstance(self.relation_type, Unset):
            relation_type = self.relation_type.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if film_id is not UNSET:
            field_dict["filmId"] = film_id
        if name_ru is not UNSET:
            field_dict["nameRu"] = name_ru
        if name_en is not UNSET:
            field_dict["nameEn"] = name_en
        if name_original is not UNSET:
            field_dict["nameOriginal"] = name_original
        if poster_url is not UNSET:
            field_dict["posterUrl"] = poster_url
        if poster_url_preview is not UNSET:
            field_dict["posterUrlPreview"] = poster_url_preview
        if relation_type is not UNSET:
            field_dict["relationType"] = relation_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        film_id = d.pop("filmId", UNSET)

        def _parse_name_ru(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name_ru = _parse_name_ru(d.pop("nameRu", UNSET))


        def _parse_name_en(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name_en = _parse_name_en(d.pop("nameEn", UNSET))


        def _parse_name_original(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name_original = _parse_name_original(d.pop("nameOriginal", UNSET))


        poster_url = d.pop("posterUrl", UNSET)

        poster_url_preview = d.pop("posterUrlPreview", UNSET)

        _relation_type = d.pop("relationType", UNSET)
        relation_type: SimilarFilmResponseItemsRelationType | Unset
        if isinstance(_relation_type,  Unset):
            relation_type = UNSET
        else:
            relation_type = SimilarFilmResponseItemsRelationType(_relation_type)




        similar_film_response_items = cls(
            film_id=film_id,
            name_ru=name_ru,
            name_en=name_en,
            name_original=name_original,
            poster_url=poster_url,
            poster_url_preview=poster_url_preview,
            relation_type=relation_type,
        )


        similar_film_response_items.additional_properties = d
        return similar_film_response_items

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

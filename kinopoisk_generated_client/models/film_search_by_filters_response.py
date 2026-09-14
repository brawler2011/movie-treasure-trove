from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.film_search_by_filters_response_items import FilmSearchByFiltersResponseItems





T = TypeVar("T", bound="FilmSearchByFiltersResponse")



@_attrs_define
class FilmSearchByFiltersResponse:
    """ 
        Attributes:
            total (int):  Example: 7.
            total_pages (int):  Example: 1.
            items (list[FilmSearchByFiltersResponseItems]):
     """

    total: int
    total_pages: int
    items: list[FilmSearchByFiltersResponseItems]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.film_search_by_filters_response_items import FilmSearchByFiltersResponseItems # noqa: PLC0415
        total = self.total

        total_pages = self.total_pages

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "total": total,
            "totalPages": total_pages,
            "items": items,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.film_search_by_filters_response_items import FilmSearchByFiltersResponseItems # noqa: PLC0415
        d = dict(src_dict)
        total = d.pop("total")

        total_pages = d.pop("totalPages")

        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = FilmSearchByFiltersResponseItems.from_dict(items_item_data)



            items.append(items_item)


        film_search_by_filters_response = cls(
            total=total,
            total_pages=total_pages,
            items=items,
        )


        film_search_by_filters_response.additional_properties = d
        return film_search_by_filters_response

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

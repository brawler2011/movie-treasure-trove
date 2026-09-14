from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.review_response_items import ReviewResponseItems





T = TypeVar("T", bound="ReviewResponse")



@_attrs_define
class ReviewResponse:
    """ 
        Attributes:
            total (int): Суммарное кол-во пользовательских рецензий Example: 12.
            total_pages (int):  Example: 2.
            total_positive_reviews (int):  Example: 1.
            total_negative_reviews (int):  Example: 7.
            total_neutral_reviews (int):  Example: 12.
            items (list[ReviewResponseItems]):
     """

    total: int
    total_pages: int
    total_positive_reviews: int
    total_negative_reviews: int
    total_neutral_reviews: int
    items: list[ReviewResponseItems]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.review_response_items import ReviewResponseItems # noqa: PLC0415
        total = self.total

        total_pages = self.total_pages

        total_positive_reviews = self.total_positive_reviews

        total_negative_reviews = self.total_negative_reviews

        total_neutral_reviews = self.total_neutral_reviews

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "total": total,
            "totalPages": total_pages,
            "totalPositiveReviews": total_positive_reviews,
            "totalNegativeReviews": total_negative_reviews,
            "totalNeutralReviews": total_neutral_reviews,
            "items": items,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.review_response_items import ReviewResponseItems # noqa: PLC0415
        d = dict(src_dict)
        total = d.pop("total")

        total_pages = d.pop("totalPages")

        total_positive_reviews = d.pop("totalPositiveReviews")

        total_negative_reviews = d.pop("totalNegativeReviews")

        total_neutral_reviews = d.pop("totalNeutralReviews")

        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ReviewResponseItems.from_dict(items_item_data)



            items.append(items_item)


        review_response = cls(
            total=total,
            total_pages=total_pages,
            total_positive_reviews=total_positive_reviews,
            total_negative_reviews=total_negative_reviews,
            total_neutral_reviews=total_neutral_reviews,
            items=items,
        )


        review_response.additional_properties = d
        return review_response

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

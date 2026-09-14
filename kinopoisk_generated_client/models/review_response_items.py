from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.review_response_items_type import ReviewResponseItemsType
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ReviewResponseItems")



@_attrs_define
class ReviewResponseItems:
    """ 
        Attributes:
            kinopoisk_id (int | Unset):  Example: 2.
            type_ (ReviewResponseItemsType | Unset):
            date (str | Unset):  Example: 2010-09-05T20:37:00.
            positive_rating (int | Unset):  Example: 122.
            negative_rating (int | Unset):  Example: 12.
            author (str | Unset):  Example: Username.
            title (None | str | Unset):  Example: Title.
            description (str | Unset):  Example: text.
     """

    kinopoisk_id: int | Unset = UNSET
    type_: ReviewResponseItemsType | Unset = UNSET
    date: str | Unset = UNSET
    positive_rating: int | Unset = UNSET
    negative_rating: int | Unset = UNSET
    author: str | Unset = UNSET
    title: None | str | Unset = UNSET
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kinopoisk_id = self.kinopoisk_id

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        date = self.date

        positive_rating = self.positive_rating

        negative_rating = self.negative_rating

        author = self.author

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if kinopoisk_id is not UNSET:
            field_dict["kinopoiskId"] = kinopoisk_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if date is not UNSET:
            field_dict["date"] = date
        if positive_rating is not UNSET:
            field_dict["positiveRating"] = positive_rating
        if negative_rating is not UNSET:
            field_dict["negativeRating"] = negative_rating
        if author is not UNSET:
            field_dict["author"] = author
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kinopoisk_id = d.pop("kinopoiskId", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: ReviewResponseItemsType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = ReviewResponseItemsType(_type_)




        date = d.pop("date", UNSET)

        positive_rating = d.pop("positiveRating", UNSET)

        negative_rating = d.pop("negativeRating", UNSET)

        author = d.pop("author", UNSET)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))


        description = d.pop("description", UNSET)

        review_response_items = cls(
            kinopoisk_id=kinopoisk_id,
            type_=type_,
            date=date,
            positive_rating=positive_rating,
            negative_rating=negative_rating,
            author=author,
            title=title,
            description=description,
        )


        review_response_items.additional_properties = d
        return review_response_items

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

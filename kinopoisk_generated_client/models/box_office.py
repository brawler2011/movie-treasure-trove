from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="BoxOffice")



@_attrs_define
class BoxOffice:
    """ 
        Attributes:
            type_ (str):  Example: BUDGET.
            amount (int):  Example: 63000000.
            currency_code (str):  Example: USD.
            name (str):  Example: US Dollar.
            symbol (str):  Example: $.
     """

    type_: str
    amount: int
    currency_code: str
    name: str
    symbol: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        amount = self.amount

        currency_code = self.currency_code

        name = self.name

        symbol = self.symbol


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "amount": amount,
            "currencyCode": currency_code,
            "name": name,
            "symbol": symbol,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        amount = d.pop("amount")

        currency_code = d.pop("currencyCode")

        name = d.pop("name")

        symbol = d.pop("symbol")

        box_office = cls(
            type_=type_,
            amount=amount,
            currency_code=currency_code,
            name=name,
            symbol=symbol,
        )


        box_office.additional_properties = d
        return box_office

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.distribution_sub_type import DistributionSubType
from ..models.distribution_type import DistributionType
from typing import cast

if TYPE_CHECKING:
  from ..models.company import Company
  from ..models.distribution_country import DistributionCountry





T = TypeVar("T", bound="Distribution")



@_attrs_define
class Distribution:
    """ 
        Attributes:
            type_ (DistributionType):  Example: PREMIERE.
            sub_type (DistributionSubType):  Example: CINEMA.
            date (None | str):  Example: 1999-05-07.
            re_release (bool | None):  Example: False.
            country (DistributionCountry):
            companies (list[Company]):
     """

    type_: DistributionType
    sub_type: DistributionSubType
    date: None | str
    re_release: bool | None
    country: DistributionCountry
    companies: list[Company]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.company import Company # noqa: PLC0415
        from ..models.distribution_country import DistributionCountry # noqa: PLC0415
        type_ = self.type_.value

        sub_type = self.sub_type.value

        date: None | str
        date = self.date

        re_release: bool | None
        re_release = self.re_release

        country = self.country.to_dict()

        companies = []
        for companies_item_data in self.companies:
            companies_item = companies_item_data.to_dict()
            companies.append(companies_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "subType": sub_type,
            "date": date,
            "reRelease": re_release,
            "country": country,
            "companies": companies,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.company import Company # noqa: PLC0415
        from ..models.distribution_country import DistributionCountry # noqa: PLC0415
        d = dict(src_dict)
        type_ = DistributionType(d.pop("type"))




        sub_type = DistributionSubType(d.pop("subType"))




        def _parse_date(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        date = _parse_date(d.pop("date"))


        def _parse_re_release(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        re_release = _parse_re_release(d.pop("reRelease"))


        country = DistributionCountry.from_dict(d.pop("country"))




        companies = []
        _companies = d.pop("companies")
        for companies_item_data in (_companies):
            companies_item = Company.from_dict(companies_item_data)



            companies.append(companies_item)


        distribution = cls(
            type_=type_,
            sub_type=sub_type,
            date=date,
            re_release=re_release,
            country=country,
            companies=companies,
        )


        distribution.additional_properties = d
        return distribution

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

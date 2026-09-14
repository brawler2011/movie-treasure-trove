from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.filters_response_countries import FiltersResponseCountries
  from ..models.filters_response_genres import FiltersResponseGenres





T = TypeVar("T", bound="FiltersResponse")



@_attrs_define
class FiltersResponse:
    """ 
        Attributes:
            genres (list[FiltersResponseGenres]):
            countries (list[FiltersResponseCountries]):
     """

    genres: list[FiltersResponseGenres]
    countries: list[FiltersResponseCountries]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.filters_response_countries import FiltersResponseCountries # noqa: PLC0415
        from ..models.filters_response_genres import FiltersResponseGenres # noqa: PLC0415
        genres = []
        for genres_item_data in self.genres:
            genres_item = genres_item_data.to_dict()
            genres.append(genres_item)



        countries = []
        for countries_item_data in self.countries:
            countries_item = countries_item_data.to_dict()
            countries.append(countries_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "genres": genres,
            "countries": countries,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filters_response_countries import FiltersResponseCountries # noqa: PLC0415
        from ..models.filters_response_genres import FiltersResponseGenres # noqa: PLC0415
        d = dict(src_dict)
        genres = []
        _genres = d.pop("genres")
        for genres_item_data in (_genres):
            genres_item = FiltersResponseGenres.from_dict(genres_item_data)



            genres.append(genres_item)


        countries = []
        _countries = d.pop("countries")
        for countries_item_data in (_countries):
            countries_item = FiltersResponseCountries.from_dict(countries_item_data)



            countries.append(countries_item)


        filters_response = cls(
            genres=genres,
            countries=countries,
        )


        filters_response.additional_properties = d
        return filters_response

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

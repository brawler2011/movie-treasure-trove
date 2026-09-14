from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.api_key_response_account_type import ApiKeyResponseAccountType
from typing import cast

if TYPE_CHECKING:
  from ..models.api_key_response_daily_quota import ApiKeyResponseDailyQuota
  from ..models.api_key_response_total_quota import ApiKeyResponseTotalQuota





T = TypeVar("T", bound="ApiKeyResponse")



@_attrs_define
class ApiKeyResponse:
    """ 
        Attributes:
            total_quota (ApiKeyResponseTotalQuota):
            daily_quota (ApiKeyResponseDailyQuota):
            account_type (ApiKeyResponseAccountType):  Example: FREE.
     """

    total_quota: ApiKeyResponseTotalQuota
    daily_quota: ApiKeyResponseDailyQuota
    account_type: ApiKeyResponseAccountType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.api_key_response_daily_quota import ApiKeyResponseDailyQuota # noqa: PLC0415
        from ..models.api_key_response_total_quota import ApiKeyResponseTotalQuota # noqa: PLC0415
        total_quota = self.total_quota.to_dict()

        daily_quota = self.daily_quota.to_dict()

        account_type = self.account_type.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "totalQuota": total_quota,
            "dailyQuota": daily_quota,
            "accountType": account_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_key_response_daily_quota import ApiKeyResponseDailyQuota # noqa: PLC0415
        from ..models.api_key_response_total_quota import ApiKeyResponseTotalQuota # noqa: PLC0415
        d = dict(src_dict)
        total_quota = ApiKeyResponseTotalQuota.from_dict(d.pop("totalQuota"))




        daily_quota = ApiKeyResponseDailyQuota.from_dict(d.pop("dailyQuota"))




        account_type = ApiKeyResponseAccountType(d.pop("accountType"))




        api_key_response = cls(
            total_quota=total_quota,
            daily_quota=daily_quota,
            account_type=account_type,
        )


        api_key_response.additional_properties = d
        return api_key_response

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

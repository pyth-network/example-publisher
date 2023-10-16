from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlatformFee")


@_attrs_define
class PlatformFee:
    """
    Attributes:
        amount (Union[Unset, str]):
        fee_bps (Union[Unset, int]):
    """

    amount: Union[Unset, str] = UNSET
    fee_bps: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        fee_bps = self.fee_bps

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if fee_bps is not UNSET:
            field_dict["feeBps"] = fee_bps

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        fee_bps = d.pop("feeBps", UNSET)

        platform_fee = cls(
            amount=amount,
            fee_bps=fee_bps,
        )

        platform_fee.additional_properties = d
        return platform_fee

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.swap_info import SwapInfo


T = TypeVar("T", bound="RoutePlanStep")


@_attrs_define
class RoutePlanStep:
    """
    Attributes:
        swap_info (SwapInfo):
        percent (int):
    """

    swap_info: "SwapInfo"
    percent: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        swap_info = self.swap_info.to_dict()

        percent = self.percent

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "swapInfo": swap_info,
                "percent": percent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.swap_info import SwapInfo

        d = src_dict.copy()
        swap_info = SwapInfo.from_dict(d.pop("swapInfo"))

        percent = d.pop("percent")

        route_plan_step = cls(
            swap_info=swap_info,
            percent=percent,
        )

        route_plan_step.additional_properties = d
        return route_plan_step

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

from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SwapResponse")


@_attrs_define
class SwapResponse:
    """
    Attributes:
        swap_transaction (str):
        last_valid_block_height (float):
    """

    swap_transaction: str
    last_valid_block_height: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        swap_transaction = self.swap_transaction
        last_valid_block_height = self.last_valid_block_height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "swapTransaction": swap_transaction,
                "lastValidBlockHeight": last_valid_block_height,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        swap_transaction = d.pop("swapTransaction")

        last_valid_block_height = d.pop("lastValidBlockHeight")

        swap_response = cls(
            swap_transaction=swap_transaction,
            last_valid_block_height=last_valid_block_height,
        )

        swap_response.additional_properties = d
        return swap_response

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

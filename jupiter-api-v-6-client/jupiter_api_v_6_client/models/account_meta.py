from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountMeta")


@_attrs_define
class AccountMeta:
    """
    Attributes:
        pubkey (str):
        is_signer (bool):
        is_writable (bool):
    """

    pubkey: str
    is_signer: bool
    is_writable: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pubkey = self.pubkey
        is_signer = self.is_signer
        is_writable = self.is_writable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pubkey": pubkey,
                "isSigner": is_signer,
                "isWritable": is_writable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pubkey = d.pop("pubkey")

        is_signer = d.pop("isSigner")

        is_writable = d.pop("isWritable")

        account_meta = cls(
            pubkey=pubkey,
            is_signer=is_signer,
            is_writable=is_writable,
        )

        account_meta.additional_properties = d
        return account_meta

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

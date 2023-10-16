from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_meta import AccountMeta


T = TypeVar("T", bound="Instruction")


@_attrs_define
class Instruction:
    """
    Attributes:
        program_id (str):
        accounts (List['AccountMeta']):
        data (str):
    """

    program_id: str
    accounts: List["AccountMeta"]
    data: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        program_id = self.program_id
        accounts = []
        for accounts_item_data in self.accounts:
            accounts_item = accounts_item_data.to_dict()

            accounts.append(accounts_item)

        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "programId": program_id,
                "accounts": accounts,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_meta import AccountMeta

        d = src_dict.copy()
        program_id = d.pop("programId")

        accounts = []
        _accounts = d.pop("accounts")
        for accounts_item_data in _accounts:
            accounts_item = AccountMeta.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        data = d.pop("data")

        instruction = cls(
            program_id=program_id,
            accounts=accounts,
            data=data,
        )

        instruction.additional_properties = d
        return instruction

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

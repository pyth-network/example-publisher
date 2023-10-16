from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SwapInfo")


@_attrs_define
class SwapInfo:
    """
    Attributes:
        amm_key (str):
        input_mint (str):
        output_mint (str):
        in_amount (str):
        out_amount (str):
        fee_amount (str):
        fee_mint (str):
        label (Union[Unset, str]):
    """

    amm_key: str
    input_mint: str
    output_mint: str
    in_amount: str
    out_amount: str
    fee_amount: str
    fee_mint: str
    label: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amm_key = self.amm_key
        input_mint = self.input_mint
        output_mint = self.output_mint
        in_amount = self.in_amount
        out_amount = self.out_amount
        fee_amount = self.fee_amount
        fee_mint = self.fee_mint
        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ammKey": amm_key,
                "inputMint": input_mint,
                "outputMint": output_mint,
                "inAmount": in_amount,
                "outAmount": out_amount,
                "feeAmount": fee_amount,
                "feeMint": fee_mint,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amm_key = d.pop("ammKey")

        input_mint = d.pop("inputMint")

        output_mint = d.pop("outputMint")

        in_amount = d.pop("inAmount")

        out_amount = d.pop("outAmount")

        fee_amount = d.pop("feeAmount")

        fee_mint = d.pop("feeMint")

        label = d.pop("label", UNSET)

        swap_info = cls(
            amm_key=amm_key,
            input_mint=input_mint,
            output_mint=output_mint,
            in_amount=in_amount,
            out_amount=out_amount,
            fee_amount=fee_amount,
            fee_mint=fee_mint,
            label=label,
        )

        swap_info.additional_properties = d
        return swap_info

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

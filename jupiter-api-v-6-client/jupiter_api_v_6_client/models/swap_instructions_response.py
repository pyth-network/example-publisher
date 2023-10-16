from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instruction import Instruction


T = TypeVar("T", bound="SwapInstructionsResponse")


@_attrs_define
class SwapInstructionsResponse:
    """
    Attributes:
        compute_budget_instructions (List['Instruction']): The necessary instructions to setup the compute budget.
        setup_instructions (List['Instruction']): Setup missing ATA for the users.
        swap_instruction (Instruction):
        address_lookup_table_addresses (List[str]): The lookup table addresses that you can use if you are using
            versioned transaction.
        token_ledger_instruction (Union[Unset, Instruction]):
        cleanup_instruction (Union[Unset, Instruction]):
    """

    compute_budget_instructions: List["Instruction"]
    setup_instructions: List["Instruction"]
    swap_instruction: "Instruction"
    address_lookup_table_addresses: List[str]
    token_ledger_instruction: Union[Unset, "Instruction"] = UNSET
    cleanup_instruction: Union[Unset, "Instruction"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        compute_budget_instructions = []
        for compute_budget_instructions_item_data in self.compute_budget_instructions:
            compute_budget_instructions_item = compute_budget_instructions_item_data.to_dict()

            compute_budget_instructions.append(compute_budget_instructions_item)

        setup_instructions = []
        for setup_instructions_item_data in self.setup_instructions:
            setup_instructions_item = setup_instructions_item_data.to_dict()

            setup_instructions.append(setup_instructions_item)

        swap_instruction = self.swap_instruction.to_dict()

        address_lookup_table_addresses = self.address_lookup_table_addresses

        token_ledger_instruction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.token_ledger_instruction, Unset):
            token_ledger_instruction = self.token_ledger_instruction.to_dict()

        cleanup_instruction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cleanup_instruction, Unset):
            cleanup_instruction = self.cleanup_instruction.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "computeBudgetInstructions": compute_budget_instructions,
                "setupInstructions": setup_instructions,
                "swapInstruction": swap_instruction,
                "addressLookupTableAddresses": address_lookup_table_addresses,
            }
        )
        if token_ledger_instruction is not UNSET:
            field_dict["tokenLedgerInstruction"] = token_ledger_instruction
        if cleanup_instruction is not UNSET:
            field_dict["cleanupInstruction"] = cleanup_instruction

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instruction import Instruction

        d = src_dict.copy()
        compute_budget_instructions = []
        _compute_budget_instructions = d.pop("computeBudgetInstructions")
        for compute_budget_instructions_item_data in _compute_budget_instructions:
            compute_budget_instructions_item = Instruction.from_dict(compute_budget_instructions_item_data)

            compute_budget_instructions.append(compute_budget_instructions_item)

        setup_instructions = []
        _setup_instructions = d.pop("setupInstructions")
        for setup_instructions_item_data in _setup_instructions:
            setup_instructions_item = Instruction.from_dict(setup_instructions_item_data)

            setup_instructions.append(setup_instructions_item)

        swap_instruction = Instruction.from_dict(d.pop("swapInstruction"))

        address_lookup_table_addresses = cast(List[str], d.pop("addressLookupTableAddresses"))

        _token_ledger_instruction = d.pop("tokenLedgerInstruction", UNSET)
        token_ledger_instruction: Union[Unset, Instruction]
        if isinstance(_token_ledger_instruction, Unset):
            token_ledger_instruction = UNSET
        else:
            token_ledger_instruction = Instruction.from_dict(_token_ledger_instruction)

        _cleanup_instruction = d.pop("cleanupInstruction", UNSET)
        cleanup_instruction: Union[Unset, Instruction]
        if isinstance(_cleanup_instruction, Unset):
            cleanup_instruction = UNSET
        else:
            cleanup_instruction = Instruction.from_dict(_cleanup_instruction)

        swap_instructions_response = cls(
            compute_budget_instructions=compute_budget_instructions,
            setup_instructions=setup_instructions,
            swap_instruction=swap_instruction,
            address_lookup_table_addresses=address_lookup_table_addresses,
            token_ledger_instruction=token_ledger_instruction,
            cleanup_instruction=cleanup_instruction,
        )

        swap_instructions_response.additional_properties = d
        return swap_instructions_response

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

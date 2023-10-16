from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.swap_mode import SwapMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.platform_fee import PlatformFee
    from ..models.route_plan_step import RoutePlanStep


T = TypeVar("T", bound="QuoteResponse")


@_attrs_define
class QuoteResponse:
    """
    Attributes:
        input_mint (str):
        in_amount (str):
        output_mint (str):
        out_amount (str):
        other_amount_threshold (str):
        swap_mode (SwapMode):
        slippage_bps (int):
        price_impact_pct (str):
        route_plan (List['RoutePlanStep']):
        platform_fee (Union[Unset, PlatformFee]):
        context_slot (Union[Unset, float]):
        time_taken (Union[Unset, float]):
    """

    input_mint: str
    in_amount: str
    output_mint: str
    out_amount: str
    other_amount_threshold: str
    swap_mode: SwapMode
    slippage_bps: int
    price_impact_pct: str
    route_plan: List["RoutePlanStep"]
    platform_fee: Union[Unset, "PlatformFee"] = UNSET
    context_slot: Union[Unset, float] = UNSET
    time_taken: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_mint = self.input_mint
        in_amount = self.in_amount
        output_mint = self.output_mint
        out_amount = self.out_amount
        other_amount_threshold = self.other_amount_threshold
        swap_mode = self.swap_mode.value

        slippage_bps = self.slippage_bps
        price_impact_pct = self.price_impact_pct
        route_plan = []
        for route_plan_item_data in self.route_plan:
            route_plan_item = route_plan_item_data.to_dict()

            route_plan.append(route_plan_item)

        platform_fee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.platform_fee, Unset):
            platform_fee = self.platform_fee.to_dict()

        context_slot = self.context_slot
        time_taken = self.time_taken

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputMint": input_mint,
                "inAmount": in_amount,
                "outputMint": output_mint,
                "outAmount": out_amount,
                "otherAmountThreshold": other_amount_threshold,
                "swapMode": swap_mode,
                "slippageBps": slippage_bps,
                "priceImpactPct": price_impact_pct,
                "routePlan": route_plan,
            }
        )
        if platform_fee is not UNSET:
            field_dict["platformFee"] = platform_fee
        if context_slot is not UNSET:
            field_dict["contextSlot"] = context_slot
        if time_taken is not UNSET:
            field_dict["timeTaken"] = time_taken

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.platform_fee import PlatformFee
        from ..models.route_plan_step import RoutePlanStep

        d = src_dict.copy()
        input_mint = d.pop("inputMint")

        in_amount = d.pop("inAmount")

        output_mint = d.pop("outputMint")

        out_amount = d.pop("outAmount")

        other_amount_threshold = d.pop("otherAmountThreshold")

        swap_mode = SwapMode(d.pop("swapMode"))

        slippage_bps = d.pop("slippageBps")

        price_impact_pct = d.pop("priceImpactPct")

        route_plan = []
        _route_plan = d.pop("routePlan")
        for route_plan_item_data in _route_plan:
            route_plan_item = RoutePlanStep.from_dict(route_plan_item_data)

            route_plan.append(route_plan_item)

        _platform_fee = d.pop("platformFee", UNSET)
        platform_fee: Union[Unset, PlatformFee]
        if not _platform_fee or isinstance(_platform_fee, Unset):
            platform_fee = UNSET
        else:
            platform_fee = PlatformFee.from_dict(_platform_fee)

        context_slot = d.pop("contextSlot", UNSET)

        time_taken = d.pop("timeTaken", UNSET)

        quote_response = cls(
            input_mint=input_mint,
            in_amount=in_amount,
            output_mint=output_mint,
            out_amount=out_amount,
            other_amount_threshold=other_amount_threshold,
            swap_mode=swap_mode,
            slippage_bps=slippage_bps,
            price_impact_pct=price_impact_pct,
            route_plan=route_plan,
            platform_fee=platform_fee,
            context_slot=context_slot,
            time_taken=time_taken,
        )

        quote_response.additional_properties = d
        return quote_response

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

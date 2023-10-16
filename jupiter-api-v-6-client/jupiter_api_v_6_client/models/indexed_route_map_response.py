from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.indexed_route_map_response_indexed_route_map import IndexedRouteMapResponseIndexedRouteMap


T = TypeVar("T", bound="IndexedRouteMapResponse")


@_attrs_define
class IndexedRouteMapResponse:
    """
    Attributes:
        mint_keys (List[str]): All the mints that are indexed to match in indexedRouteMap
        indexed_route_map (IndexedRouteMapResponseIndexedRouteMap): All the possible route and their corresponding
            output mints Example: {'1': [2, 3, 4], '2': [1, 3, 4]}.
    """

    mint_keys: List[str]
    indexed_route_map: "IndexedRouteMapResponseIndexedRouteMap"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mint_keys = self.mint_keys

        indexed_route_map = self.indexed_route_map.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mintKeys": mint_keys,
                "indexedRouteMap": indexed_route_map,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.indexed_route_map_response_indexed_route_map import IndexedRouteMapResponseIndexedRouteMap

        d = src_dict.copy()
        mint_keys = cast(List[str], d.pop("mintKeys"))

        indexed_route_map = IndexedRouteMapResponseIndexedRouteMap.from_dict(d.pop("indexedRouteMap"))

        indexed_route_map_response = cls(
            mint_keys=mint_keys,
            indexed_route_map=indexed_route_map,
        )

        indexed_route_map_response.additional_properties = d
        return indexed_route_map_response

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

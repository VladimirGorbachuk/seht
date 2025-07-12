from dataclasses import dataclass
from uuid import UUID


@dataclass
class WareHouse:
    uuid: UUID


@dataclass
class DeliveryFromTo:
    from_uuid: UUID
    to_uuid: UUID
     

@dataclass
class ItemSize:
    x: float
    y: float
    z: float


@dataclass
class Item:
    uuid: UUID
    sizes: ItemSize
    weight: float


@dataclass
class ItemQuantity:
    """
    Defines quantity of given items for
    cases such as:
     - available in warehouse
     - reserved for user cart service
    """
    item: Item
    quantity: int


class 
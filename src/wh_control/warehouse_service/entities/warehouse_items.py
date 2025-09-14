from dataclasses import dataclass
from uuid import UUID


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


@dataclass
class WareHouse:
    uuid: UUID
    item_quantities: list[ItemQuantity]

    def add_items(self, item_quantity: ItemQuantity):
        # todo: extend this item adding functionality
        self.item_quantities

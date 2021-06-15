from typing import Set, List, Union
from cLibrary.structure.item.Item import Item
from cLibrary.structure.warehouse.Area import Area


class StockRecord:

    def __init__(self, item: Item, location, qty: int):
        self.item = item
        self.location = location
        self.qty = qty

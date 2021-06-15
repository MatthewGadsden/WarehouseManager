from typing import Set, List, Union, Optional
from cLibrary.structure.item.StockRecord import StockRecord
import math


class Slot:

    def __init__(self, warehouse, slf):
        self.warehouse = warehouse 

        self.aisle = slf.aisle
        self.bay = slf.bay
        self.level = slf.level
        self.position = slf.position
        self.spot_id = slf.id

        self.suits_pick_face = slf.suits_pick_face
        self.is_pick_face = slf.is_pick_slot
        self.suits_multi_pick = slf.suits_multi_pick

        self.stock_records = []  # type: List[StockRecord]
        self.allocations = []   # type: List[StockRecord]

        self.s_height = int(slf.height)
        self.s_width = int(slf.width)
        self.s_depth = int(slf.depth)

        self.used_width = 0
        self.used_height = 0
        self.used_weight = 0

    def __eq__(self, other):
        return (self.aisle == other.aisle and
                self.bay == other.bay and
                self.level == other.level and
                self.position == other.position)

    def __gt__(self, other):
        if not isinstance(other, (Slot, )):
            raise TypeError()
        if self.aisle > other.aisle:
            return True
        elif self.bay > other.bay:
            return True
        elif self.level > other.level:
            return True
        elif self.position > other.position:
            return True
        return False

    def __lt__(self, other):
        return not (self > other)

    def _item_used_width(self, record: StockRecord, hp: int) -> int:
        """
        Calculate width used on pallet by item, given quantity
        :param record: Stock Record (item, location, qty)
        :param hp: Height percentage to use of pallet
        :return: width used (int)
        """
        item = record.item
        max_height = self.s_height * (hp / 100)

        carton_length = item.carton.length
        carton_width = item.carton.width
        carton_height = item.carton.height

        d = carton_length   # set starting depth
        h = carton_height   # set starting height
        w = carton_width    # set starting width
        c = math.ceil(record.qty / item.carton.units)   # number of cartons (rounded up)

        # Loop through cartons and simulate stack on a pallet
        for i in range(c):
            if w > self.s_width:
                return w
            if d + item.carton.length < self.s_depth:
                d += item.carton.length

            elif h + item.carton.height < max_height:
                d = item.carton.length
                h += item.carton.height
            else:
                d = item.carton.length
                h = item.carton.height
                w += item.carton.width
        return w

    def _item_used_weight(self, record: StockRecord) -> float:
        """
        Calculate item used weight, given quantity of item
        :param record: Stock Record (item, location, qty)
        :return:
        """
        w = record.item.carton.weight
        c = math.ceil(record.qty / record.item.carton.units)
        w = c * w
        return w

    def get_attrs(self, room=5, hp=80):
        room /= 100
        room += 1
        width = 0
        weight = 0
        for record in self.stock_records:
            width += self._item_used_width(record, hp=hp)*room
            weight += self._item_used_weight(record)
        self.used_width = width
        self.used_weight = weight

    def get_pick_slots(self, filt):
        """
        Get list of pick slots
        :param filt: filter to pick which pick slots are wanted
        :return:
        """
        if filt is None:
            return [self,]
        else:
            return [self,] if filt(self) else []

    def assign_item(self, item_id: str, stk):
        """
        Add item pick slots assignment to this slot
        :param item_id: Item Code being Assigned to Slot
        :param stk: Stk Data Container
        :return: None
        """
        stock_record = StockRecord(self.warehouse.item_list[item_id], self, stk.qty)
        if self.is_pick_face:
            self.allocations.append(stock_record)
            stock_record.item.allocations.append(stock_record)
        else:
            self.stock_records.append(stock_record)
            stock_record.item.stock_records.append(stock_record)

    def get_item_avehitsday(self) -> Optional[float]:
        """
        Get the average hits per day for this slots item allocations
        (Returns the average of all items, if more than 1 allocation to slot)
        :return: average hits per day (float), None if no allocations
        """
        if not self.allocations:
            return None
        else:
            c = 0
            t_ahd = 0
            for record in self.allocations:
                t_ahd += record.item.avehitsday
                c += 1
            return t_ahd / c

    def get_display_id(self) -> str:
        """
        Get printable id string
        :return: Aisle-Bay-Level-Position (string)
        """
        return str(self.aisle + '-' + self.bay + '-' + self.level + '-' + self.position)

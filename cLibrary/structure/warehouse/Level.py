from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Slot import Slot
from typing import List, Set, Union, Optional
import math
import random


class Level(Area):

    def __init__(self, slf, warehouse):
        super().__init__()
        self.warehouse = warehouse
        self.aisle = slf.aisle
        self.bay = slf.bay
        self.level = slf.level
        self.spot_id = self.aisle + self.bay + self.level

    def add_line(self, slf):
        postition = slf.position
        if postition in self:
            raise Exception("There is no way this could possibly occur within the warehouse, contact admin urgently")
        else:
            self[postition] = Slot(self.warehouse, slf)
            self.count += 1

    def get_filled_pick_slots_count(self):
        e = 0
        for slot in self:
            if slot.suits_pick_face:
                if slot.allocations:
                    e += 1
        return e

    def get_empty_pick_slots_count(self):
        e = 0
        for slot in self:
            if slot.suits_pick_face:
                if not slot.allocations:
                    e += 1
        return e

    def get_filled_pick_slots(self):
        filled = []
        for spot in self:
            if spot.suits_pick_face:
                if spot.allocations:
                    filled.append(spot)
        return filled

    def get_pick_slots(self, filt=None):
        slots = []
        for spot in self:
            if spot.suits_pick_face:
                if filt is None:
                    slots.append(spot)
                elif filt(spot):
                    slots.append(spot)
        return slots

    def get_reserve_slots(self) -> List[Slot]:
        slots = []
        for spot in self:
            if not spot.suits_pick_face:
                slots.append(spot)
        return slots

    def get_best_hits(self) -> float:
        best_hits = None
        for spot in self:
            if spot.is_pick_face:
                if best_hits is None:
                    if spot.allocations:
                        best_hits = spot.get_item_avehitsday()
                    else:
                        best_hits = None
                else:
                    if spot.allocations:
                        best_hits = max(best_hits, spot.get_item_avehitsday())
                    else:
                        pass
        return best_hits

    def get_average_hits(self):
        e = 0
        n = self.get_filled_pick_slots_count()
        for slot in self:
            if slot.item is not None:
                e += slot.get_item_avehitsday()
        return e/n

    def aux_average_hits(self):
        e = 0
        for slot in self:
            if slot.suits_pick_face:
                if slot.allocations:
                    e += slot.get_item_avehitsday()
        return e

    def get_rand_area(self):
        n = len(self.spots)
        rand = random.randint(1, n)
        for i in range(n):
            try:
                return self[(rand + i)%n]
            except KeyError:
                pass

    def find_item_location(self, item_id):
        for pickslot in self:
            if pickslot.item is not None and pickslot.item.item_id == item_id:
                return pickslot.spot_id

    def find_area(self, area_id):
        area = None
        for spot in self:
            if spot.spot_id == area_id:
                return spot
        return area

    def get_slot(self, position_code: str) -> Slot:
        return self[position_code]

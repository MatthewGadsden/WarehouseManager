from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.PickSlot import PickSlot, ReserveSlot
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
            if slf.type == "R":
                self[postition] = ReserveSlot(slf, self.warehouse)
            elif slf.type == "P":
                self[postition] = PickSlot(slf, self.warehouse)
                self.count += 1

    def get_filled_pick_slots_count(self):
        e = 0
        for slot in self:
            if slot.type == "P":
                if slot.item is not None:
                    e += 1
        return e

    def get_empty_pick_slots_count(self):
        e = 0
        for slot in self:
            if slot.type == "P":
                if slot.item is None:
                    e += 1
        return e

    def get_best_avehitsday_aux(self, bestList, used_slots):
        """
        edit to the best_avehistday auxiliary function, since this is the smallest type of area in a warehouse
        :param bestList: list of the best slots found so far
        :param used_slots: Used slots, so dont find these
        :return: best slot not yet found by the function
        """
        best_slot = self[0]
        for slot in self:
            if (slot not in bestList) and (slot not in used_slots):
                slot_best = slot.get_item_avehitsday()
                best_best = best_slot.get_item_avehitsday()
                if not (isinstance(best_best, float) or isinstance(best_best, int)):
                    best_slot = slot
                elif isinstance(slot_best, int) or isinstance(slot_best, float):
                    if slot_best > best_best:
                        best_slot = slot
        if best_slot.get_item_avehitsday() is None or best_slot in bestList or best_slot in used_slots:
            return None
        return best_slot

    def get_filled_pick_slots(self):
        filled = []
        for spot in self:
            if spot.type == "P":
                if spot.item is not None:
                    filled.append(spot)
        return filled

    def get_pick_slots(self, filt=None):
        slots = []
        for spot in self:
            if spot.type == "P":
                if filt is None:
                    slots.append(spot)
                elif filt(spot):
                    slots.append(spot)
        return slots

    def get_reserve_slots(self):
        slots = []
        for spot in self:
            if spot.type == "R":
                slots.append(spot)
        return slots

    def get_best_hits(self):
        best_hits = None
        for spot in self:
            if spot.type == "P":
                if best_hits is None:
                    if spot.item is not None:
                        best_hits = spot.item.avehitsday
                    else:
                        best_hits = None
                else:
                    if spot.item is not None:
                        best_hits = max(best_hits, spot.item.avehitsday)
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
            if slot.type == "P":
                if slot.item is not None:
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

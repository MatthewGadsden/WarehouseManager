import random
from typing import List, Tuple, Set


class Area:

    def __init__(self):
        self.spot_id = None
        self.spots = {}
        self.count = 0

    def __eq__(self, other):
        """
        Area equality testing
        :param other: Area to compare to
        :return: Boolean
        """
        if not isinstance(other, Area):
            raise TypeError("Cannot compare {} type with Area type".format(type(other)))
        return self.spot_id == other.spot_id

    def __lt__(self, other):
        """
        Area comparison testing
        :param other: Area to compare to
        :return: Boolean
        """
        if not isinstance(other, Area):
            raise TypeError("Cannot compare {} type with Area type".format(type(other)))
        return self.spot_id < other.spot_id

    def __gt__(self, other):
        """
        Area comparison testing
        :param other: Area to compare to
        :return: Boolean
        """
        if not isinstance(other, Area):
            raise TypeError("Cannot compare {} type with Area type".format(type(other)))
        return self.spot_id > other.spot_id

    def __delitem__(self, key):
        """
        Delete child area from current area
        :param key: Key to area of child
        :return: None
        """
        del self.spots[key]

    def check_duplicate(self, key):
        """
        Check if spot already exists in children of this Area
        :param key:
        :return:
        """
        if key in self.spots:
            raise KeyError("Spot already exists in the warehouse, cannot have two identical Spots")

    def get_sorted_list(self):
        spots = [*self.spots.values()]
        spots.sort()
        return spots

    def __len__(self):
        return sum(map(lambda x: len(x), self))

    def __setitem__(self, key, value):
        """
        Used to set spots
        :param key: spot number
        :param value: spot object
        """
        self.check_duplicate(key)
        self.spots[key] = value

    def __contains__(self, key):
        """
        :param key: aisle number
        :return: return True is the warehouse contains this aisle, else return False
        """
        if key in self.spots:
            return True
        else:
            return False

    def create_level(self, level_n):
        area = self.get_pick_slots()
        level = [slot for slot in area if slot.level == str(level_n)]
        return level

    def __getitem__(self, key):
        """
        :param key: aisle number
        :return: aisle object
        """
        if key in self.spots:
            return self.spots[key]
        else:
            return None

    def __iter__(self):
        return self.spots.values().__iter__()

    def get_filled_pick_slots_count(self):
        """
        Get the number of slots that have an item allocated to them
        :return: returns the total number of filled areas within this area
        # A "filled area" is a pick_slot with an item within it in this instance
        """
        e = 0
        for spot in self:
            e += spot.get_filled_pick_slots_count()
        return e

    def get_empty_pick_slots_count(self):
        """
        Get the number of slots that have an item allocated to them
        :return: returns the total number of filled areas within this area
        # A "filled area" is a pick_slot with an item within it in this instance
        """
        e = 0
        for spot in self:
            e += spot.get_empty_pick_slots_count()
        return e

    def get_best_avehitsday(self, num, used_slots=[]):
        """
        Purpose - To get the best slots according to their average hits per day
        :param num: number of slots you want
        :param used_slots: slots already used, so do not find these ones
        :return: list of the best slots according to the average hits per day of that slot
        """

        # this is done to make sure not searching for more slots than are actually filled
        filled = self.get_filled_pick_slots()
        max_i = len(filled)
        if num > max_i:
            num = max_i

        filled.sort(key=lambda x: x.get_item_avehitsday(), reverse=True)
        best_list = filled[:num]
        return best_list

    def get_best_dayxhits(self, num, used_slots=[]):
        """
        Purpose - To get the best slots according to their average hits per day

        :param num: number of slots you want
        :param used_slots: slots already used, so do not find these ones
        :return: list of the best slots according to the average hits per day of that slot
        """

        # this is done to make sure not searching for more slots than are actually filled
        filled = self.get_filled_pick_slots()
        max_i = len(filled)
        if num > max_i:
            num = max_i

        filled.sort(key=lambda x: x.item.avehitsday * (x.item.dayshit*0.3), reverse=True)
        best_list = filled[:num]
        return best_list

    def get_filled_pick_slots(self):
        """
        Get a list of all the "empty" slots in this area
        :return: List of Empty slots found in this area
        """
        filled = []
        for spot in self:
            temp = spot.get_filled_pick_slots()
            if temp is not None:
                filled += temp
        return filled

    def get_pick_slots(self, filt=None):
        """
        Get list of all slots in area
        :return: List of slots
        """
        slots = []
        for spot in self:
            slots += spot.get_pick_slots(filt)
        return slots

    def get_best_hits(self):
        """
        get best hits of position in this Area
        :return:
        """
        best_hits = None
        for area in self:
            if not isinstance(area, Area):
                raise TypeError("area Should be of type Area")
            if best_hits is None:
                best_hits = area.get_best_hits()
            else:
                temp_hits = area.get_best_hits()
                if temp_hits is None:
                    pass
                else:
                    best_hits = max(best_hits, temp_hits)
        return best_hits

    def get_average_hits(self):
        """
        get average hits of all filled positions in this Area
        :return: float of average hits
        """
        try:
            total = 0
            for spot in self:
                total += spot.aux_average_hits()
            n = self.get_filled_pick_slots_count()
            return total/n
        except ZeroDivisionError:
            return 0

    def aux_average_hits(self):
        """
        get average hits of all filled positions in this Area
        :return: float of average hits
        """
        total = 0
        for spot in self:
            total += spot.aux_average_hits()
        return total

    def find_item_reserves(self, item_id):
        """
        Find reserve slots of an Item
        :param item_id: Item id string
        :return: List[ReserveSlot]
        """
        slots = []
        reserves = self.get_reserve_slots()
        for res in reserves:
            for item in res.items:
                if item.item_id == item_id:
                    slots.append(res.spot_id)
        return slots

    def get_reserve_slots(self):
        """
        Get list of reserve slots
        :return: List[Slot]
        """
        slots = []
        for spot in self:
            slots += spot.get_reserve_slots()
        return slots

    def find_area(self, area_id):
        """
        find an area
        :param area_id: area id that needs to be matched
        :return:
        """
        if self.spot_id == area_id:
            return self
        for spot in self.spots.values():
            area = spot.find_area(area_id)
            if area is not None:
                return area
        return None

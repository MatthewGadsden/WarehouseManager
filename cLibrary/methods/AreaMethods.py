from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Aisle import Aisle
from cLibrary.structure.warehouse.Bay import Bay
from cLibrary.structure.warehouse.Level import Level
from cLibrary.structure.warehouse.Slot import Slot
from cLibrary.structure.item.Item import Item

from cLibrary.methods.general import *
import pandas as pd
import datetime
import math
import csv
import copy
from typing import Set, List, Tuple


def check_nested_area(area1, area2, warehouse):
    if not isinstance(area1, (Aisle, Bay, Level, Slot)) and not isinstance(area2, (Aisle, Bay, Level, Slot)):
        raise TypeError("area must be of Type Aisle, Bay, Level")

    area1_len = len(area1.spot_id)
    area2_len = len(area2.spot_id)
    dif = area1_len - area2_len

    if dif > 0:
        path = area1.spot_id[:area2_len]
        current = area2.spot_id
        if current == path:
            raise ValueError("area, or part of area already exists in CustomArea")
    elif dif < 0:
        path = area2.spot_id[:area1_len]
        current = area1.spot_id
        if current == path:
            raise ValueError("area, or part of area already exists in CustomArea")
    else:
        if area1.spot_id == area2.spot_id:
            raise ValueError("area, or part of area already exists in CustomArea")


def sorted_1_4(area, method):
    """
    Make sure best items are on the 2nd and 3rd levels of picking
    """
    area_spots = area.get_pick_slots()  # type: List[Slot]
    cat_items = area.get_filled_pick_slots()  # type: List[Slot]

    l_23 = area.get_pick_slots(filt=lambda spot: spot.level in ["2", "3"])  # type: List[Slot]

    n_23 = len(l_23)
    cat_items.sort(key=lambda slot: slot.get_item_avehitsday())

    best_items = cat_items[:n_23]
    worst_items = cat_items[n_23:]

    i = 0
    while i < len(best_items):
        if best_items[i].level in ["2", "3"]:
            best_items.pop(i)
            i -= 1
        i += 1

    i = 0
    while i < len(worst_items):
        if worst_items[i].level in ["1", "4"]:
            worst_items.pop(i)
            i -= 1
        i += 1

    l_23_empty = area.get_pick_slots(filt=lambda spot: spot.level in ["2", "3"] and not spot.allocations)  # type: List[Slot]
    worst_areas = l_23_empty + worst_items  # type: List[Slot]

    worst_areas.sort(key=lambda x: x.spot_id)
    best_items.sort(key=lambda x: x.spot_id)

    moves = []
    while len(best_items) > 0:
        moves.append((best_items.pop(0), worst_areas.pop(0)))

    return moves


def best_sort_1_4(area):
    return sorted_1_4(area, Area.get_best_avehitsday)


def dayxhits_sort_1_4(area):
    return sorted_1_4(area, Area.get_best_dayxhits)


def ground_con(area, bay_range=10, gap=5, hp=80) -> List[List[Slot]]:
    bay_range = int(bay_range)
    gap = int(gap)

    if not isinstance(area, Area):
        raise TypeError()

    reserves = area.get_reserve_slots()     # type: List[ReserveSlot]
    reserves.sort(key=lambda x: x.spot_id)
    for i in reserves:
        i.get_attrs(gap, hp)

    gap /= 100
    gap += 1

    _ = 0  # removing the empty reserve slots
    while _ < len(reserves):
        if not reserves[_].stock_records:
            reserves.pop(_)
            _ -= 1
        _ += 1

    i = 0
    consolidations = []
    while i < len(reserves):
        j = i
        current_slot = reserves.pop(i)
        current_con = [current_slot, ]
        while j < len(reserves) and len(current_con) < 2 and j < i + bay_range + 1:
            if current_slot.used_width + reserves[j].used_width < current_slot.s_width:
                current_con.append(reserves.pop(j))
                consolidations.append(current_con)
            j += 1

    return consolidations

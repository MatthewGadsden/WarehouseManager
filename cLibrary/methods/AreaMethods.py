from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Aisle import Aisle
from cLibrary.structure.warehouse.Bay import Bay
from cLibrary.structure.warehouse.Level import Level
from cLibrary.structure.warehouse.PickSlot import PickSlot, ReserveSlot
from cLibrary.structure.item.Item import Item

from cLibrary.methods.general import *
import pandas as pd
import datetime
import math
import csv
import copy
from typing import Set, List, Tuple


def check_nested_area(area1, area2, warehouse):
    if not isinstance(area1, (Aisle, Bay, Level, PickSlot)) and not isinstance(area2, (Aisle, Bay, Level, PickSlot)):
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
    area_spots = area.get_pick_slots()  # type: List[PickSlot]
    cat_items = area.get_filled_pick_slots()  # type: List[PickSlot]

    l_23 = area.get_pick_slots(filt=lambda spot: spot.level in ["2", "3"])  # type: List[PickSlot]

    n_23 = len(l_23)
    cat_items.sort(key=lambda slot: slot.item.avehitsday)

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

    l_23_empty = area.get_pick_slots(filt=lambda spot: spot.level in ["2", "3"] and spot.item is None)  # type: List[PickSlot]
    worst_areas = l_23_empty + worst_items  # type: List[PickSlot]

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


def ground_con(area, bay_range=10, gap=10):
    bay_range = int(bay_range)
    gap = int(gap)
    gap /= 100
    gap += 1

    if not isinstance(area, Area):
        raise TypeError()
    total_cons = []
    cons = []

    reserves = area.get_reserve_slots()
    reserves.sort(key=lambda x: x.spot_id)

    _ = 0  # removing the empty reserve slots
    while _ < len(reserves):
        if reserves[_].items == []:
            reserves.pop(_)
            _ -= 1
        _ += 1

    i = 0
    while i < len(reserves):
        breaking = False
        s1 = reserves[i]
        if not isinstance(s1, ReserveSlot):
            raise TypeError()

        j = i + 1
        while j < len(reserves) and (int(s1.bay) > (int(reserves[j].bay) - bay_range)):
            s2 = reserves[j]
            if not isinstance(s2, ReserveSlot):
                raise TypeError()

            if (s1.s_current_width + s2.s_current_width) < s1.s_width:
                k = j + 1
                while (k < len(reserves)) and ((int(s1.bay) > (int(reserves[k].bay) - bay_range))):
                    s3 = reserves[k]
                    if not isinstance(s3, ReserveSlot):
                        raise TypeError()

                    if (s1.s_current_width + s2.s_current_width + s3.s_current_width) < s1.s_width:
                        cons.append([s1, s2, s3])
                        breaking = True
                        reserves.pop(k), reserves.pop(j), reserves.pop(i)
                        i -= 1
                        break
                    k += 1
            if breaking:
                break
            j += 1
        i += 1
    total_cons.append(cons)

    cons2 = []
    i = 0
    while i < len(reserves):
        s1 = reserves[i]
        if not isinstance(s1, ReserveSlot):
            raise TypeError()

        j = i + 1
        while j < len(reserves) and (int(s1.bay) > (int(reserves[j].bay) - bay_range)):
            s2 = reserves[j]
            if not isinstance(s2, ReserveSlot):
                raise TypeError()

            if (s1.s_current_width + s2.s_current_width) < s1.s_width:
                breaking = True
                cons2.append([s1, s2])
                reserves.pop(i), reserves.pop(j-1)
                i -= 1
                break
            j += 1
        i += 1
    total_cons.append(cons2)
    return total_cons


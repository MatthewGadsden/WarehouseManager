from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Aisle import Aisle
from cLibrary.structure.warehouse.Bay import Bay
from cLibrary.structure.warehouse.Level import Level
from cLibrary.structure.warehouse.PickSlot import PickSlot, ReserveSlot
from cLibrary.structure.item.Item import *
from typing import List, Tuple, Set
from cLibrary.structure.datatypes.Category import Category
from cLibrary.structure.warehouse.CustomArea import CustomArea
import pandas as pd


def relay(category, area, excess_area, controller, outfile):
    category = category     # type: Category
    area = area     # type: CustomArea
    excess_area = excess_area  # type: CustomArea

    cat_items = category.get_items()  # type: List[Item]

    # Building the lists of pick slots to fill
    area_spots_23_b = area.get_pick_slots(
        filt=lambda x: x.aisle in ["BB", ] and x.level in ["2", "3"] and x.pick_slot in ["1", "2", "3", "4"])  # type: List[PickSlot]

    area_spots_23_c = area.get_pick_slots(
        filt=lambda x: x.aisle in ["CC", ] and x.level in ["2", "3"] and x.pick_slot in ["1", "2", "3", "4"])  # type: List[PickSlot]

    area_spots_14 = area.get_pick_slots(
        filt=lambda x: x.level in ["4", ] and x.pick_slot in ["1", "2", "3", "4"])  # type: List[PickSlot]

    excess_spots = excess_area.get_pick_slots()  # type: List[PickSlot]

    cat_items.sort(key=lambda x: x.get_inner_vol(), reverse=True)    # sorting items by volume (size)
    area_spots_23_b.sort(key=lambda x: x.spot_id, reverse=True) # sort B aisle in reverse
    area_spots_23_c.sort(key=lambda x: x.spot_id)   # sort C aisle normally

    area_spots_23 = area_spots_23_b + area_spots_23_c   # merge aisles B and C

    area_spots_14.sort(key=lambda x: x.spot_id, reverse=True)

    for item in cat_items:
        print(item.get_inner_vol())

    for spot in area_spots_23:
        print(spot.spot_id)

    for spot in area_spots_14:
        print(spot.spot_id)

    pairings = []   # type: List[Tuple[Item, PickSlot]]
    while len(cat_items) > 0 and len(area_spots_23) > 0:
        pairings.append((cat_items.pop(0), area_spots_23.pop(0)))

    while len(cat_items) > 0 and len(area_spots_14) > 0:
        pairings.append((cat_items.pop(0), area_spots_14.pop(0)))
    sheet1 = []

    for item, slot in pairings:
        sheet1.append([item.pick_slot.spot_id if item.pick_slot is not None else "No Location", item.item_id,
                       item.pick_slot.qty if item.pick_slot is not None else 0, "", slot.spot_id, "", ])

    df1 = pd.DataFrame(sheet1, columns=['Current Location', 'Item ID',
                                        'Qty', 'Qty Check', 'New Location', 'Moved Check', ])
    writer = pd.ExcelWriter(outfile)
    df1.to_excel(writer, 'Sheet1')
    writer.save()
    return outfile

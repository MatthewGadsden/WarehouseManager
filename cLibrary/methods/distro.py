from typing import List, Tuple, Set
from cLibrary.structure.item.Item import Item
from cLibrary.structure.warehouse.Warehouse import Warehouse
from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Slot import Slot
from cLibrary.methods.general import create_xlsx, xlsx_ft, data_to_dataframe, dataframes_to_xlsx
from cLibrary.methods.slotReport import pick_slot_report
import math


def get_facings_width(item: Item, qty: int, max_depth: int = 1200, max_height: int = 1400):
    """
    Get width of facings in a distro setup
    :param item: Item
    :param qty: qty of item
    :param max_depth: maximum depth a each facing can be
    :param max_height: maximum height a facing can be
    :return: width of facings needed for item in distro
    """
    w = item.carton.width   # type: int
    d = 0   # type: int
    h = 0   # type: int
    c = math.ceil(qty / item.carton.units)  # type: int

    # simulates stacking of cartons to get the facings width
    while c > 0:
        c -= 1
        d += item.carton.length
        if d > max_depth:
            d = 0
            h += item.carton.height

        if h > max_height:
            h = 0
            w += item.carton.width

    return w


def distro_setup(distro_data: List[Tuple[Item, int]], area: Area, warehouse: Warehouse, output_file: str) -> str:
    """
    Create excel sheets to setup a distro order
    :param distro_data: list of items and their qty's
    :param area: Area to allocate Pick Slots to (assuming that pick slots are empty)
    :param warehouse: warehouse data
    :param output_file: output file destination
    :return: File name
    """

    # getting facing width data
    data = []
    item_list = []
    for i, (itm, qty) in enumerate(distro_data):
        facing_w = get_facings_width(itm, qty) * 1.1
        data.append(distro_data[i] + (facing_w,))
        item_list.append(itm)

    pick_slots = area.get_pick_slots()  # type: List[Slot]
    pick_slots.sort(key=lambda x: x.position)
    pick_slots.sort(key=lambda x: x.level)
    pick_slots.sort(key=lambda x: int(x.bay))

    bay = []
    bays = []
    current_bay = None
    for slot in pick_slots:
        if slot.bay != current_bay:
            if len(bay) > 0:
                bays.append(bay)
                bay = []
            current_bay = slot.bay
        bay.insert(0, slot)

    current_width = 0
    bay = 0
    for i, item in enumerate(data):
        if (current_width + item[2]) > 2550 or len(bays[bay]) == 0:
            bay += 1
            current_width = 0
        current_width += item[2]
        location = bays[bay].pop()
        data[i] = [item[0].item_id, item[1], item[2],
                   location.aisle, location.bay, location.level, location.position]

    output_file = xlsx_ft(output_file)
    dfs = [data_to_dataframe(data, ['ITEM ID', 'QTY', 'FACING WIDTH', 'Aisle', 'Bay', 'Level', 'Position']),
           pick_slot_report(item_list)]
    dataframes_to_xlsx(dfs=dfs, outfile=output_file)
    return output_file

import pandas as pd
from typing import List, Tuple, Set
from cLibrary.structure.item.Item import Item
from cLibrary.methods.general import data_to_dataframe


def pick_slot_report(items: List[Item]) -> [str, pd.DataFrame]:
    data = []

    data = [[item.item_id,
             record.location.aisle,
             record.location.bay,
             record.location.level,
             record.location.position,
             record.qty, ""] for item in items for record in item.allocations]
    return data_to_dataframe(data, ['ITEM ID', 'Aisle', 'Bay', 'Level', 'Position', 'QTY', 'ACTUAL QTY'])


def reserve_slot_report(items: List[Item]) -> pd.DataFrame:
    pass

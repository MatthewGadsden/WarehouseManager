import pandas as pd
from typing import List, Tuple, Set
from cLibrary.structure.item.Item import Item


def pick_slot_report(items: List[Item]) -> pd.DataFrame:
    data = [[item.item_id, (item.pick_slot.spot_id if item.pick_slot is not None else "None"),
             item.pick_slot.qty if item.pick_slot is not None else 0, ""] for item in items]
    df = pd.DataFrame(data=data, columns=['ITEM ID', 'SLOT ID', 'QTY', 'ACTUAL QTY'])
    return df


def reserve_slot_report(items: List[Item]) -> pd.DataFrame:
    pass

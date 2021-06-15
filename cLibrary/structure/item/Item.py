from cLibrary.structure.datatypes.LineFormat import ILF
from typing import List, Set, Union


class Item:

    def __init__(self, ilf, hl, warehouse):
        # ['Urbane Quince+Blueberry 125ml Diffuser', 'Seasonal', 'DIFFUSER', nan, '125ml', nan,
        # 'URBA4', 'Urbane', 'SHAD', 'Shadows']
        self.item_id = ilf.item_id
        self.total_qty = ilf.qty
        self.hits = 0
        self.avehitsday = 0
        self.dayshit = 0
        self.pmax = ilf.pmax
        self.lettrigger = ilf.lettrigger

        self.carton = Carton(ilf.length_pc, ilf.width_pc, ilf.height_pc, ilf.weight_pc, ilf.units_pc)
        self.inner = Inner(ilf.length_pi, ilf.width_pi, ilf.height_pi, ilf.weight_pi, ilf.units_pi)
        self.unit = Unit(ilf.length_pu, ilf.width_pu, ilf.height_pu, ilf.weight_pu, 1)
        self.barcode1 = ilf.barcode1
        self.barcode2 = ilf.barcode2

        self.allocations = []
        self.stock_records = []

        if hl is not None and hl is not False:
            self.hits = hl.hits
            self.avehitsday = hl.avehitsday
            self.dayshit = hl.dayshit

    def get_unit_vol(self):
        unit = self.unit
        return (unit.width * unit.length * unit.height) / (1000000000)

    def get_inner_vol(self):
        inner = self.inner
        vol = (inner.width * inner.length * inner.height) / (1000000000)

        if vol == float(0):
            return self.get_unit_vol()

        return vol


class Packet:
    def __init__(self, length, width, height, weight, units):
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.units = units


class Unit(Packet):
    def __init__(self, *args, **kwargs):
        super(Unit, self).__init__(*args, **kwargs)


class Inner(Packet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Carton(Packet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ItemList:

    def __init__(self, filename, hits_hash, warehouse):
        self.count = 0
        self.warehouse = warehouse
        self.hits_hash = hits_hash
        self.items = {}
        self.item_list = []
        self.read_item_data(filename)

    def read_item_data(self, filename):
        f = open(filename)
        fline = True
        name_indexing = {}
        for line in f:
            if fline:
                line1 = line.strip('\n').replace('"', '').split(",")
                for i, name in enumerate(line1):
                    name_indexing[name] = i
                fline = False
            else:
                self.add_line(line, name_indexing)
        f.close()

    def add_line(self, line, indexing):
        ilf = ILF(line, indexing)
        item_id = ilf.item_id
        try:
            item_hlf = self.hits_hash[item_id]
        except:
            item_hlf = None
        item = Item(ilf, item_hlf, self.warehouse)
        self[item_id] = item
        self.count += 1

    def __contains__(self, item_id):
        return item_id in self.items

    def __setitem__(self, item_id, item):
        if self.items.get(item_id) is not None:  # IMPORTANT! - without this items will be doubled up!
            self.item_list.remove(self.items[item_id])
        self.items[item_id] = item
        self.item_list.append(item)

    def __iter__(self):
        return self.items.__iter__()

    def __getitem__(self, item_id):
        return self.items[item_id]

    def __len__(self):
        return self.count

    def get_item(self, item_id):
        return self.items[item_id]

from cLibrary.structure.warehouse.Aisle import Aisle
from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.item.Item import ItemList
from cLibrary.structure.datatypes.LineFormat import SltLF, StkLF, HLF


class Warehouse(Area):

    def __init__(self, item_file, slot_file, stock_file, hits_file):
        super().__init__()
        self.spot_id = "Ladelle"
        hits_hash = self.hash_hits(hits_file)
        self.read_slot_file(slot_file)
        self.item_list = ItemList(item_file, hits_hash, self)
        self.assign_ps_items(stock_file)

    def add_line(self, line, indexing):
        """
        This will import data into the aisles and create a new aisle if there isn't an aisle matching the line data
        :param line: line being imported into the warehouse
        :param indexing: indexing for item attributes
        """
        slf = SltLF(line, indexing)
        aisle = slf.aisle
        if aisle in self:
            self[aisle].add_line(slf)
        else:
            self[aisle] = Aisle(slf, self)
            self.count += 1
            self[aisle].add_line(slf)

    def read_slot_file(self, filename):
        """
        importing slots from file
        :param filename: file to import
        :return: None
        """
        f = open(filename)
        name_indexing = {}
        fline = True
        for line in f:
            if fline:
                line1 = line.strip('\n').replace('"', '').split(",")
                for i, name in enumerate(line1):
                    name_indexing[name] = i
                fline = False
            else:
                self.add_line(line, name_indexing)
        f.close()

    @staticmethod
    def hash_hits(hits_file):
        """
        import file for item hits
        :param hits_file: file to import
        :return: dictionary of item_id: item hits data
        """
        h = {}
        name_indexing = {}
        fline = True
        f = open(hits_file)
        for line in f:
            if fline:
                line1 = line.strip('\n').replace('"', '').split(",")
                for i, name in enumerate(line1):
                    name_indexing[name] = i
                fline = False
            else:
                x = HLF(line, name_indexing)
                h[x.item_id] = x
        f.close()
        return h

    def assign_ps_items(self, filename):
        """
        assigning items to pick slots
        :param filename:
        :return: None
        """
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
                self.assign_item(line, name_indexing)
        f.close()

    def assign_item(self, line, indexing):
        stock_obj = StkLF(line, indexing)
        item_id = stock_obj.item_id
        slot = self[stock_obj.aisle][stock_obj.bay][stock_obj.level][stock_obj.position]
        slot.assign_item(item_id, stock_obj)

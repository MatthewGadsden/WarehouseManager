import re


class LF:
    def __init__(self):
        pass


class SltLF(LF):

    def __init__(self, line, indexing):
        super().__init__()
        psp2 = re.compile("[0-9]{5}[A-D]")
        line = line.strip('\n').replace('"', '').split(",")

        self.loccode = line[indexing['loccode']].replace(" ", "")
        self.aisle = line[indexing['aisle']].replace(" ", "").zfill(2)
        self.bay = line[indexing['bay']].replace(" ", "")
        self.level = line[indexing['level']].replace(" ", "")
        self.position = line[indexing['position']].replace(" ", "")
        self.id = self.aisle + self.bay + self.level + self.position

        self.active = False
        if line[indexing['activ']] != "N":
            self.active = True

        self.suits_pick_face = line[indexing['okpickslot']].replace(" ", "") == "T"
        self.status = line[indexing['frzstock']]
        self.is_pick_slot = line[indexing['ispickslot']] == "T"
        self.suits_multi_pick = line[indexing['multiitmpk']] == "T"

        self.height = line[indexing['shgt']]
        self.width = line[indexing['width']]
        self.depth = line[indexing['sdepth']]


class ILF(LF):
    def __init__(self, line, indexing):
        super().__init__()
        line = line.strip('\n').replace('"', '').replace(" ", "").split(",")
        self.item_id = line[indexing['itm']]
        self.qty = float(line[indexing['qty']])
        self.barcode1 = line[indexing['apn']]
        self.barcode2 = line[indexing['tun']]

        self.length_pc = int(line[indexing['l']])
        self.width_pc = int(line[indexing['w']])
        self.height_pc = int(line[indexing['h']])
        self.weight_pc = float(line[indexing['wgt']])
        self.units_pc = int(line[indexing['spk']])

        self.length_pi = int(line[indexing['l_inner']])
        self.width_pi = int(line[indexing['w_inner']])
        self.height_pi = int(line[indexing['h_inner']])
        self.weight_pi = float(line[indexing['wgt_inner']])
        self.units_pi = int(line[indexing['spk_inner']])

        self.length_pu = int(line[indexing['l2']])
        self.width_pu = int(line[indexing['w2']])
        self.height_pu = int(line[indexing['h2']])
        self.weight_pu = float(line[indexing['wg2']])

        self.pmax = int(line[indexing['pmax']])
        self.lettrigger = int(line[indexing['lettrigger']])


class StkLF(LF):
    def __init__(self, line, indexing):
        super().__init__()
        line = line.strip('\n').replace('"', '').replace(" ", "").split(",")
        self.item_id = line[indexing['sitm']].replace(" ", "")
        self.loccode = line[indexing['loccode']].replace(" ", "")
        self.aisle = line[indexing['aisle']].replace(" ", "").zfill(2)
        self.bay = line[indexing['bay']].replace(" ", "")
        self.level = line[indexing['level']].replace(" ", "")
        self.position = line[indexing['position']].replace(" ", "")
        self.id = self.aisle + self.bay + self.level + self.position
        self.status = line[indexing['status']]
        self.type = line[indexing['slottype']] if line[indexing['slottype']] != "" else "P"
        self.qty = float(line[indexing['sqty']])


class HLF(LF):
    def __init__(self, line, indexing):
        super().__init__()
        line = line.strip('\n').replace('"', '').replace(" ", "").split(",")
        self.item_id = line[indexing['item']]
        self.hits = float(line[indexing['hits']])
        self.avehitsday = float(line[indexing['aveunitday']])
        self.dayshit = float(line[indexing['dayshit']])

from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.item.Item import ReserveProduct


class PickSlot:

    def __init__(self, slf, warehouse):
        self.warehouse = warehouse
        self.spot_id = slf.id
        self.aisle = slf.aisle
        self.bay = slf.bay
        self.level = slf.level
        self.pick_slot = slf.position
        self.item = None
        self.type = slf.type
        self.qty = 0
        self.active = slf.ispickslot

    def __len__(self):
        return 1

    def __eq__(self, other):
        return self.spot_id == other.spot_id

    def __lt__(self, other):
        return self.spot_id < other.spot_id

    def __gt__(self, other):
        return self.spot_id > other.spot_id

    def get_slots(self):
        return [self]

    def clean(self):
        if self.item is not None:
            self.item.pick_slot = None
            self.item = None

    def assign_item(self, item_id, stk):
        self.item = self.warehouse.item_list[item_id]
        if self.active:
            self.item.pick_slot = self
        self.qty = stk.qty

    def switch_item_slot(self, item, qty=0):
        self.qty = (item.pick_slot.qty if item.pick_slot is not None else qty)
        if item.pick_slot is not None:
            item.pick_slot.item = None
        self.item = item
        item.pick_slot = self

    def get_filled_slots(self):
        return [self] if self.item is not None else None

    def get_pick_slots(self, filt):
        if filt is None:
            return [self,]
        else:
            return [self,] if filt(self) else []

    def get_filled_pick_slots(self):
        if self.item is not None:
            return [self,]

    def get_item_id(self):
        if self.item is None:
            return None
        else:
            return self.item.item_id

    def get_item_range(self):
        if self.item is None:
            return None
        else:
            return self.item.range

    def get_item_type(self):
        if self.item is None:
            return None
        else:
            return self.item.type

    def get_item_brand(self):
        if self.item is None:
            return None
        else:
            return self.item.brand

    def get_item_customer(self):
        if self.item is None:
            return None
        else:
            return self.item.customer

    def get_item_hits(self):
        if self.item is None:
            return None
        else:
            return self.item.hits

    def get_item_avehitsday(self):
        if self.item is None:
            return None
        else:
            return self.item.avehitsday

    def get_item_dayshit(self):
        if self.item is None:
            return None
        else:
            return self.item.dayshit


class ReserveSlot(Area):

    def __init__(self, slf, warehouse):
        super(ReserveSlot, self).__init__()
        self.warehouse = warehouse
        self.spot_id = slf.id
        self.aisle = slf.aisle
        self.bay = slf.bay
        self.level = slf.level
        self.pick_slot = slf.position
        self.type = slf.type

        self.og_height = 1500
        self.s_width = 1100
        self.s_length = 1100
        self.s_height = 1500
        self.s_max_height = 1500
        self.s_max_weight = 500000

        self.s_current_width = 0
        self.s_current_weight = 0

        self.c = None
        self.items = []

    def get_attrs(self, room=5, hp=70):
        room /= 100
        room += 1
        self.s_height = self.og_height * (hp/100)
        width = 0
        weight = 0
        c = 0
        for item in self.items:
            width += self.P_getWidthUsed(item)*room
            weight += self.P_getWeightUsed(item)
            c += item.c_qty
        self.s_current_width = width
        self.s_current_weight = weight
        self.c = c

    def assign_item(self, item_id, stk):
        self.items.append(ReserveProduct(self.warehouse.item_list[item_id], stk.qty))

    def P_getWidthUsed(self, r_item):
        if not isinstance(r_item, ReserveProduct):
            raise TypeError("r_item must be a reserve product Type")

        l = r_item.carton.length
        h = r_item.carton.height
        w = r_item.carton.width
        c = r_item.c_qty

        for i in range(c):
            if w > self.s_width:
                return w
            if l + r_item.carton.length < self.s_length:
                l += r_item.carton.length

            elif h + r_item.carton.height < self.s_height:
                l = r_item.carton.length
                h += r_item.carton.height

            else:
                l = r_item.carton.length
                h = r_item.carton.height
                w += r_item.carton.width
        return w

    def P_getWeightUsed(self, r_item):
        if not isinstance(r_item, ReserveProduct):
            raise TypeError("r_item must be a reserve product Type")
        w = r_item.carton.weight
        c = r_item.c_qty

        w = c * w
        return w


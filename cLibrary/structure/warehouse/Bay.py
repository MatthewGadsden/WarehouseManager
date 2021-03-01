from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Level import Level


class Bay(Area):

    def __init__(self, slf, warehouse):
        super().__init__()
        self.warehouse = warehouse
        self.aisle = slf.aisle
        self.bay = slf.bay
        self.spot_id = self.aisle + self.bay

    def add_line(self, slf):
        """
        import a bay into this Aisle
        :param slf: Bay information
        :return: None
        """
        level = slf.level
        if level in self:
            self[level].add_line(slf)
        else:
            self[level] = Level(slf, self.warehouse)
            self.count += 1
            self[level].add_line(slf)

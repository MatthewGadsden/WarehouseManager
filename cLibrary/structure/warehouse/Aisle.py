from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Bay import Bay


class Aisle(Area):

    def __init__(self, slf, warehouse):
        """
        Initialise an Aisle
        :param slf:
        :param warehouse:
        """
        super().__init__()
        self.warehouse = warehouse
        self.aisle = slf.aisle
        self.spot_id = slf.aisle

    def add_line(self, slf):
        """
        import a bay into this Aisle
        :param slf: Bay information
        :return: None
        """
        bay = slf.bay
        if bay in self:
            self[bay].add_line(slf)
        else:
            self[bay] = Bay(slf, self.warehouse)
            self.count += 1
            self[bay].add_line(slf)

    def get_bay(self, bay_code: str) -> Bay:
        return self[bay_code]

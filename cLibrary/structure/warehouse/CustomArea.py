from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Aisle import Aisle
from cLibrary.structure.warehouse.Bay import Bay
from cLibrary.structure.warehouse.Level import Level
from cLibrary.methods.AreaMethods import *


class CustomArea(Area):

    def __init__(self, areas, area_name, warehouse):
        """
        Creates a "Custom Area" this is an area that doesn't have to contain solely one type of Area
        (eg Aisles only contain bay) CustomAreas can contain Aisles, Bays, Levels, other CustomAreas. It can be
        any mix and match of any of those types
        :param areas: the areas to combine to make a CustomArea
        """

        if not isinstance(areas, list):
            raise TypeError("areas needs to be of Type list, which contains objects of Type Area")
        super().__init__()

        self.area_name = area_name
        self.warehouse = warehouse

        for area in areas:
            self.area_error(area)
            self.add_spot(area)

    def area_error(self, area):
        self.light_area_error(area)
        for spot in self.spots:
            check_nested_area(self[spot], area, self.warehouse)

    def error_check(self, area):
        for j in area:
            for i in self:
                check_nested_area(j, i, self.warehouse)

    def add_spot(self, area):
        self.spots[area.spot_id] = area

    def light_area_error(self, area):
        if not isinstance(area, (Aisle, Bay, Level, CustomArea, Slot)):
            raise TypeError("area must be of Type Aisle, Bay, Level or another CustomArea")

    def __add__(self, other):
        self.area_error(other)
        self.add_spot(other)

    def __sub__(self, other):
        self.light_area_error(other)
        try:
            del self.spots[other.spot_id]
        except ValueError:
            raise ValueError("Area being removed from the Custom Area does not exist within the Custom Area.")

    def remove(self, area):
        if area.spot_id in self:
            del self[area.spot_id]
            return
        raise ValueError("Area being removed from the Custom Area does not exist within the Custom Area.")

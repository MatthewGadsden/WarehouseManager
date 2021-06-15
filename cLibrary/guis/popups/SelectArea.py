from tkinter import *
from cLibrary.structure.warehouse.Area import Area
from cLibrary.structure.warehouse.Slot import Slot
from cLibrary.structure.warehouse.Level import Level
from cLibrary.structure.warehouse.Bay import Bay
from cLibrary.structure.warehouse.Aisle import Aisle
from cLibrary.widgets.AreaCheckbox import AreaCheckbutton
from cLibrary.methods.general import center_to_win
from cLibrary.guis.popups.PickSlotSettings import PickSlotSettings


class SelectArea(Toplevel):

    def __init__(self, master, area, selecting=True):
        """
        Initialise view warehouse popup
        :param master: master window
        :param area: Warehouse location to view into
        :param selecting: Boolean (are areas being selected)
        """
        if not isinstance(area, (Area, Slot)):
            raise TypeError("area must be a type of Area")
        super(SelectArea, self).__init__(master)
        self.selecting = selecting
        if isinstance(area, Slot):
            PickSlotSettings(master, area)
            self.destroy()
        else:
            self.area = area.get_sorted_list()
            if isinstance(area, Level):
                self.area.sort(key=lambda x: int(x.position))
            else:
                self.area.sort(key=lambda x: x.spot_id)
            self.grid_row = 0
            self.grid_col = 0
            self.selected_areas = []

            self.load_area()
            self.load_settings()
            self.grab_set()

    def load_settings(self):
        """
        Load popup config
        :return: None
        """
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        center_to_win(self, self.master)

    def get_area(self, areas=None):
        """
        Attempt to push areas into system
        :param areas: areas to push (if None check selected boxes)
        :return: None
        """
        if areas is None:
            areas = []
            for box in self.selected_areas:
                areas.append(box.get()) if box.get() is not None else None
            self.get_area(areas)
        else:
            self.on_close()
            self.master.get_area(areas)

    def load_area(self):
        """
        Load display of current area being viewed
        :return: None
        """
        for spot in self.area:
            fill = 1
            emp = 1
            if not isinstance(spot, Slot):
                fill = spot.get_filled_pick_slots_count()
                emp = spot.get_empty_pick_slots_count()
            if fill != 0 or emp != 0:
                spot_str = spot.spot_id
                if isinstance(spot, Aisle):
                    spot_str = spot.aisle
                elif isinstance(spot, Bay):
                    spot_str = spot.bay
                elif isinstance(spot, Level):
                    spot_str = spot.level
                elif isinstance(spot, Slot):
                    spot_str = spot.position

                label = Button(self, text=str(type(spot).__name__)+" "+spot_str, relief="groove", bg="thistle1", width=13,
                               command=lambda e=spot: SelectArea(self, e, self.selecting))
                label.grid(row=self.grid_row, column=self.grid_col, pady=(0,2), padx=0)
                if self.selecting:
                    check_box = AreaCheckbutton(self, spot, onvalue=1, offvalue=0)
                    check_box.grid(row=self.grid_row, column=self.grid_col+1, pady=(0,2), padx=0, sticky=N+S+E+W)
                    self.selected_areas.append(check_box)
                (self.grid_col, self.grid_row) = (0, self.grid_row + 1) if self.grid_col == 2 else (2, self.grid_row)
        if self.selecting:
            select_area = Button(self, text="Select Area", relief="groove", bg="olivedrab1",
                                 command=lambda : self.get_area())
            select_area.grid(row=(self.grid_row if self.grid_col == 0 else self.grid_row + 1),
                             column=0, columnspan=4, sticky=N+S+E+W)

    def on_close(self):
        """
        Close popup protocol
        :return: None
        """
        self.master.grab_set()
        self.destroy()
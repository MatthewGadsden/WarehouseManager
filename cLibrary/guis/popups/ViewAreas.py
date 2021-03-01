from tkinter import *
from cLibrary.guis.popups.SelectArea import SelectArea
from cLibrary.methods.general import center_to_win


class ViewAreas(Toplevel):

    def __init__(self, master, areas, selecting=True, *args, **kwargs):
        """
        Initialise view warehouse popup
        :param master: master window
        :param areas: Warehouse location to view into
        :param selecting: True/False (are areas needed to be selected)
        """
        super(ViewAreas, self).__init__(master, *args, **kwargs)
        self.selecting = selecting
        self.grid_row = 0
        self.grid_col = 0
        for area in areas:
            label = Button(self, text=area.area_name, relief="groove", bg="thistle1", width=13,
                           command=lambda e=area: SelectArea(self, e, self.selecting))
            label.grid(row=self.grid_row, column=self.grid_col, pady=(0, 2), padx=0)
            (self.grid_col, self.grid_row) = (0, self.grid_row + 1) if self.grid_col == 1 else (1, self.grid_row)
        center_to_win(self, self.master.master)
        self.resizable(False, False)
        self.grab_set()
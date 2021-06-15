from cLibrary.guis.popups.StandardPopup import *
from cLibrary.guis.popups.ErrorWindow import ErrorWindow
from cLibrary.guis.popups.SelectArea import SelectArea


class NewAreaPopUp(StandardPopUp):

    def __init__(self, master, controller, area=None, *args, **kwargs):
        """
        Initialise from super class
        :param master: master window
        :param controller: program controller
        :param area: Warehouse area (None if creating new area)
        """
        self.save_string = self.save_area(area)
        self.og = False
        if area is None:
            from cLibrary.structure.warehouse.CustomArea import CustomArea
            area = CustomArea([], "", controller.warehouse)
        else:
            self.og = True
        self.area = area
        super(NewAreaPopUp, self).__init__(master, controller, *args, **kwargs)

    def load_display(self):
        """
        Load area display
        :return: None
        """
        self.area_dict = {}
        for area in self.area:
            self.area_dict[area.spot_id] = area

        self.combo_options = [key for key in self.area_dict]
        self.start_val = StringVar(self)
        try:
            self.start_val.set(self.combo_options[0])
        except IndexError:
            self.start_val.set("")

        name_label = Label(self, text="Name: ", bg="light grey", relief="groove")
        name_label.place(x=40, y=40, width=60, height=20)

        self.name_var = StringVar()
        self.name_var.set(self.area.area_name)

        name_entry = Entry(self, textvariable=self.name_var)
        name_entry.place(x=100, y=40, width=90, height=20)

        locs_label = Label(self, text="Locations: ", bg="dark grey", relief="groove")
        locs_label.place(x=40, y=60, width=60, height=30)

        self.locs_combo = Combobox(self, textvariable=self.start_val, values=self.combo_options, state='readonly')
        self.locs_combo.place(x=100, y=60, width=90, height=30)

        add_button = Button(self, text="Add", bg="chartreuse2", command=lambda: SelectArea(self, self.controller.warehouse))
        add_button.place(x=40, y=90, width=75, height=20)

        delete_button = Button(self, text="Delete", bg="orange red", command=lambda: self.delete_location())
        delete_button.place(x=115, y=90, width=75, height=20)

        ok_button = Button(self, text="Ok", bg="chartreuse2", relief="groove",
                           command=lambda: (self.ok()))
        ok_button.place(y=self.winfo_height() - 50, x=40 + 73 + 4, width=73, height=30)

        cancel_but = Button(self, text="Cancel", bg="gray70", relief="groove",
                            command=lambda: self.on_close())
        cancel_but.place(y=self.winfo_height() - 50, x=40, width=72, height=30)

    def delete_location(self):
        """
        Delete location from the current area
        :return: None
        """
        try:
            area = self.area_dict[self.start_val.get()]
            self.area - area
            self.area_dict.pop(self.start_val.get())
            self.update_combos()
        except KeyError as e:
            ErrorWindow(self, e, 'U002',)

    def get_area(self, areas):
        """
        Add locations to the warehouse area
        :param areas: locations to add to area
        :return: None
        """
        for area in areas:
            try:
                self.area + area
                self.area_dict[area.spot_id] = area
            except ValueError as e:
                error = ErrorWindow(self, e, "U003", "User Error: Spot Id {} area, or part of this area already exists "
                                    "within CustomArea location".format(area.spot_id))
                self.wait_window(error)
        self.update_combos()

    def update_combos(self):
        """
        update area combobox
        :return:
        """
        self.combo_options = [key for key in self.area_dict]
        try:
            self.start_val.set(self.combo_options[0])
        except IndexError:
            self.start_val.set("")
        self.locs_combo['values'] = self.combo_options
        self.locs_combo['textvariable'] = self.start_val

    def ok(self):
        """
        Save edits to the Area
        :return: None
        """
        try:
            if self.name_var.get() == "":
                raise ValueError("Area Name Error: Area must have a name\nEnter an Area Name")
            if not self.og:
                self.area.area_name = self.name_var.get()
                self.master.add_new(self.area)
            else:
                for area in self.controller.areas.values():
                    if area.area_name != self.area.area_name:
                        self.area.error_check(area)
                self.area.area_name = self.name_var.get()
                self.master.update_combo()
            self.on_close(cancel=False)
        except ValueError as e:
            ErrorWindow(self, e, 'U003', e)

    def on_close(self, cancel=True):
        super(NewAreaPopUp, self).on_close()
        if cancel:
            saved_area = self.load_area(self.save_string)
            for area in self.controller.areas.values():
                if area.area_name == saved_area.area_name:
                    self.controller.areas[area.area_name] = saved_area
                    break
            self.master.update_combo()

    @staticmethod
    def save_area(area) -> str:
        if area is None:
            return ""
        save_string = ""
        save_string += area.area_name
        for spot in area:
            save_string += ("," + spot.spot_id)
        return save_string

    def load_area(self, save_string: str):
        from cLibrary.structure.warehouse.CustomArea import CustomArea
        warehouse = self.controller.warehouse
        save = save_string.strip("\n").split(",")
        spots = []
        for i in save[1:]:
            spots.append(warehouse.find_area(i))
        return CustomArea(spots, save[0], warehouse)

from cLibrary.guis.popups.StandardPopup import *
from cLibrary.guis.popups.ErrorWindow import ErrorWindow
from cLibrary.guis.popups.NewAreaPopUp import NewAreaPopUp


class AreasPopUp(StandardPopUp):

    def __init__(self, master, controller, *args, **kwargs):
        """
        Initialise from super class
        :param master: master window
        :param controller: program controller
        """
        controller.save_areas()
        super(AreasPopUp, self).__init__(master, controller, *args, **kwargs)

    def load_display(self):
        """
        Loading popup display information
        :return: None
        """
        self.area_dict = {}

        for area in self.controller.areas.values():
            self.area_dict[area.area_name] = area

        self.combo_options = [key for key in self.area_dict]
        self.start_val = StringVar(self)
        try:
            self.start_val.set(list(self.controller.areas.values())[0].area_name)
        except IndexError:
            self.start_val.set("")

        areas_title = Label(self, text="Areas", bg="light grey", relief="groove")
        areas_title.place(x=40, y=40, width=150, height=20)
        self.combo = Combobox(self, values=self.combo_options, textvariable=self.start_val,
                              font="bold 10", state='readonly')
        self.combo.place(x=40, y=60, width=150, height=30)
        edit_button = Button(self, text="Edit", bg="light goldenrod", relief="groove",
                             command=lambda: NewAreaPopUp(self, controller=self.controller, area=self.area_dict[self.start_val.get()]))
        edit_button.place(x=40, y=90, width=75, height=20)
        delete_button = Button(self, text="Delete", bg="orange red", relief="groove", command=self.delete_area)
        delete_button.place(x=115, y=90, width=75, height=20)

        create_new_but = Button(self, text="Create New Area", bg="chartreuse2", relief="groove",
                           command=lambda: NewAreaPopUp(self, controller=self.controller))
        create_new_but.place(y=125, x=40, width=150, height=30)

        cancel_but = Button(self, text="Cancel", bg="gray70", relief="groove",
                           command=lambda: self.on_close())
        cancel_but.place(y=self.winfo_height() - 50, x=40, width=72, height=30)

        ok_button = Button(self, text="Ok", bg="chartreuse2", relief="groove", command=lambda:(self.on_close(cancel=False)))
        ok_button.place(y=self.winfo_height()-50, x=40+73+4, width=73, height=30)

    def delete_area(self):
        """
        Remove area from warehouse
        :return: None
        """
        try:
            area = self.area_dict[self.start_val.get()]
            self.controller.areas.pop(area.area_name, None)
            self.area_dict.pop(self.start_val.get())
            self.combo_options = [key for key in self.area_dict]
        except KeyError as e:
            ErrorWindow(self, e, 'U002')

        try:
            self.start_val.set(list(self.controller.areas.values())[0].area_name)
        except IndexError as e:
            self.start_val.set("")

        self.combo['values'] = self.combo_options
        self.combo['textvariable'] = self.start_val

    def on_close(self, cancel=True):
        super(AreasPopUp, self).on_close()
        if cancel:
            self.controller.load_areas()

    def add_new(self, area):
        """
        Add new area to warehouse
        :param area: New Area
        :return: None
        """
        a_names = []
        for a in self.controller.areas.values():
            a_names.append(a.area_name)
            a.error_check(area)  # check for any overlap errors
        if area.area_name in a_names:
            raise ValueError('Area Name Error: Area name is duplicated, use different area name')

        self.controller.areas[area.area_name] = area
        self.area_dict[area.area_name] = area
        self.combo_options = [key for key in self.area_dict]
        self.start_val.set(list(self.controller.areas.values())[0].area_name)
        self.combo['values'] = self.combo_options
        self.combo['textvariable'] = self.start_val

    def update_combo(self):
        """
        Update areas combobox
        :return: None
        """
        self.area_dict = {}

        for area in self.controller.areas.values():
            self.area_dict[area.area_name] = area

        self.combo_options = [key for key in self.area_dict]
        self.start_val = StringVar(self)
        self.start_val.set(list(self.controller.areas.values())[0].area_name)
        self.combo['values'] = self.combo_options
        self.combo['textvariable'] = self.start_val
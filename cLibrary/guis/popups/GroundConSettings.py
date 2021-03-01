from cLibrary.guis.popups.StandardPopup import *
from cLibrary.guis.popups.ErrorWindow import ErrorWindow


class GroundConSettings(StandardPopUp):

    def __init__(self, master, controller, *args, **kwargs):
        """
        Initialise from super
        :param master: master window
        :param controller: program controller
        """
        super(GroundConSettings, self).__init__(master, controller, width=230, height=105, cen_win=master.master.master, *args, **kwargs)

    def load_display(self):
        """
        Load popup display
        :return: None
        """
        gap_text = Label(self, text="Percentage Gap :", anchor=E)
        gap_text.place(x=5, y=5, width=125)
        gap_entry = Entry(self)
        gap_entry.insert(0, self.controller.gap)
        gap_entry.place(x=130, y=5, width=90)

        bay_text = Label(self, text="Bay Range :", anchor=E)
        bay_text.place(x=5, y=30, width=125)
        bay_entry = Entry(self)
        bay_entry.insert(0, self.controller.bay_range)
        bay_entry.place(x=130, y=30, width=90)

        hp_text = Label(self, text="Height Percentage :", anchor=E)
        hp_text.place(x=5, y=55, width=125)
        hp_entry = Entry(self)
        hp_entry.insert(0, self.controller.hp)
        hp_entry.place(x=130, y=55, width=90, height=20)

        ok_button = Button(self, text="Save", bg="SteelBlue1",
                           command=lambda: self.save(gap_entry, bay_entry, hp_entry))
        ok_button.place(x=180, y=80, width=40, height=20)

    def save(self, gap, bay, hp):
        """
        Save consolidation settings
        :param gap: Gap % between cartons
        :param bay: how many bats to look forward
        :param hp: height %
        :return: None
        """
        try:
            temp_hp = self.controller.hp
            temp_gap = self.controller.gap
            self.controller.bay_range = int(bay.get())

            if (temp_hp != int(hp.get())) or (temp_gap != int(gap.get())):
                self.controller.hp = int(hp.get())
                self.controller.gap = int(gap.get())
                reserves = self.controller.warehouse.get_reserve_slots()
                for spot in reserves:
                    spot.get_attrs(room=self.controller.gap)
            self.on_close()
        except ValueError as error:
            ErrorWindow(self,error,'U001')

from tkinter import *
from cLibrary.widgets.controlPanel.DSP import DSP
from cLibrary.methods.general import center_to_win


class PickSlotSettings(Toplevel):

    def __init__(self, master, slot):
        """
        Initialise popup
        :param master: master window
        :param slot: pick slot to display
        """
        super(PickSlotSettings, self).__init__(master)
        self.area = slot
        self.load_settings()
        self.grab_set()
        dsp = DSP(self, self.area, width=180, height=130)
        dsp.place(x=10, y=10)

    def load_settings(self):
        """
        Load popup config
        :return:
        """
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # self.configure(width=200, height=200)
        center_to_win(self, self.master)

    def on_close(self):
        """
        Close popup protocol
        :return:
        """
        self.master.grab_set()
        self.destroy()

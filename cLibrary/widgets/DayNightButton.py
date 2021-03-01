from tkinter import *


class DayNightButton(Button):

    def __init__(self, master, *args, **kwargs):
        super(DayNightButton, self).__init__(master, *args, **kwargs)
        self.configure(text="\uD83C\uDF19", bg="gray26", fg="light goldenrod", command=self.switch_state)
        self.night = False

    def switch_state(self):
        if self.night:
            self.master.daynight(False)
            self.configure(text="\uD83C\uDF19", bg="gray26", fg="light goldenrod")
        else:
            self.master.daynight(True)
            self.configure(text="\u2600\uFE0F", bg="snow", fg="goldenrod", anchor=W)
        self.night = not self.night
from tkinter import *


class AreaCheckbutton(Checkbutton):

    def __init__(self, master, area, *args, **kwargs):
        """
        Initiliase check button
        :param master: master window
        :param area: area link
        """
        super(AreaCheckbutton, self).__init__(master, *args, **kwargs)
        self['onvalue'] = 1
        self['offvalue'] = 0
        self.var = IntVar(self)
        self['variable'] = self.var
        self.area = area

    def get(self):
        """
        get area link
        :return: area that is linked
        """
        if self.var.get() == 1:
            return self.area
        else:
            return None

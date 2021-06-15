from cLibrary.guis.windows.WidgetWindow import *
from cLibrary.guis.popups.GroundConSettings import GroundConSettings
from cLibrary.widgets.ToolTip import CreateToolTip
from cLibrary.widgets.WinOutput import WinOutput
from cLibrary.methods.AreaMethods import ground_con
from cLibrary.methods.general import intersperse
import datetime
import pandas as pd


class MGCons(WidgetWindow):

    def __init__(self, master, controller):
        """
        initialize from super class
        :param master: master window
        :param controller: program controller
        """
        super(MGCons, self).__init__(master, controller)

    def load_title(self, text="Consolidation Program", bg="burlywood1", relief="groove"):
        super(MGCons, self).load_title(text=text, bg=bg, relief=relief)

    def load_display(self):
        """
        load window display
        :return: None
        """
        self.area_dict = {}
        self.file_path = None

        for aisle in self.controller.warehouse:
            if len(aisle.get_reserve_slots()) > 0:
                self.area_dict[str(aisle.aisle)] = aisle

        settings = Button(self, text="\u2699\uFE0F", bg="light grey", fg="grey25", font="bold 16",
                          command=lambda: GroundConSettings(self, self.controller))
        settings.place(x=10, y=70, height=40, width=40)

        CreateToolTip(settings, "change consolidation\n settings", c_off=30)

        self.output = WinOutput(self, width=870, height=self.controller.wig_height - 80,
                                x=self.controller.wig_width - 870 - 20, y=70,
                                wrap=WORD, bg="snow", font="none 10", relief="groove")
        values = [*self.area_dict.keys()]
        values.sort()
        self.combo_options = [key for key in values]

        self.start_val = StringVar(self)
        self.start_val.set(self.combo_options[0])

        bg = Label(self)

        sort_area = Frame(self)
        sort_area.place(x=60, y=70, width=210, height=100)
        sort_area.grid_rowconfigure((0, 1, 2), weight=2)
        sort_area.grid_columnconfigure(1, weight=0)
        sort_area.grid_columnconfigure(0, weight=1)

        gc_label = Label(sort_area, text="Ground Con", bg="cornflower blue", font="bold 10")
        gc_label.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        combo_title = Label(sort_area, text="Aisle", bg="light grey", font="bold 10")
        combo_title.grid(row=1, column=0, sticky=NSEW)

        sort_button = Button(sort_area, text="Consolidate", relief="groove", bg="maroon1", font="bold 10",
                             command=lambda: self.ground_con(self.area_dict[self.start_val.get()]))
        sort_button.grid(row=1, column=1, sticky=NSEW)

        self.combo = Combobox(sort_area, values=self.combo_options, textvariable=self.start_val,
                              font="bold 10", state="readonly")
        self.combo.grid(row=2, column=0, sticky=NSEW)

        open_button = Button(sort_area, text="Open", relief="groove", bg="chartreuse2", font="bold 10",
                             command=lambda: self.open_file())
        open_button.grid(row=2, column=1, sticky=NSEW)
        sort_area.update()
        bg.place(x=sort_area.winfo_x() - 2, y=sort_area.winfo_y() - 2, width=sort_area.winfo_width() + 4,
                 height=sort_area.winfo_height() + 4)

        bg2 = Label(self)
        warehouse_reports = Frame(self)
        warehouse_reports.place(x=sort_area.winfo_x(), y=sort_area.winfo_y() + sort_area.winfo_height() + 10,
                                width=sort_area.winfo_width(), height=90)
        warehouse_reports.grid_columnconfigure(0, weight=1)
        warehouse_reports.grid_rowconfigure(0, weight=1)
        warehouse_reports.grid_rowconfigure(1, weight=2)
        if True:
            title = Label(warehouse_reports, text="Get Warehouse Report", bg="cornflower blue", font="bold 10")
            title.grid(row=0, column=0, sticky=NSEW)

            sort_button = Button(warehouse_reports, text="Print Report", relief="groove", bg="maroon1",
                                 command=lambda: self.ground_report(), font="bold 10")
            sort_button.grid(row=1, column=0, sticky=NSEW)
            pass
        warehouse_reports.update()
        bg2.place(x=warehouse_reports.winfo_x() - 2, y=warehouse_reports.winfo_y() - 2,
                  width=warehouse_reports.winfo_width() + 4, height=warehouse_reports.winfo_height() + 4)
        pass

    def open_file(self):
        """
        open most recently created excel doc
        :return: None (prints update to Output console)
        """
        try:
            self.output.r_insert("Opening file...")
            self.output.update()
            if self.file_path is None:
                assert False, "ObjectError: No consolidations run yet"
            else:
                os.system('start excel.exe "{}"'.format(self.file_path))
        except AssertionError as e:
            self.output.r_insert(e)

    def ground_con(self, area):
        """
        run ground con and create excel file
        :param area: area to consolidate
        :return: None (prints update in output console)
        """
        self.output.r_insert("Working out Consolidations...\n")
        self.output.update()
        cons = ground_con(area, self.controller.bay_range, self.controller.gap, self.controller.hp)

        report = []
        for i in cons:
            temp = []
            for idx, a in enumerate(i):
                i[idx] = a.spot_id
                temp.append(a.aisle)
                temp.append(a.bay)
                temp.append(a.level)
                temp.append(a.position)
                temp.append("")
            report.append(temp)

        for idx, a in enumerate(cons):
            cons[idx] = intersperse(cons[idx], "")

        df = pd.DataFrame(report, columns=["Aisle", "Bay", "Level", "Position", "Check1", "Aisle", "Bay", "Level", "Position", "Check2"])

        now = datetime.datetime.now()
        date = "{0}-{1}-{2}".format(now.day, now.month, now.year)
        output = "Ground_A{1}-CON-{0}.xlsx".format(date, area.aisle)
        self.file_path = "resources/output/" + output
        writer = pd.ExcelWriter(self.file_path)

        df.to_excel(writer, 'Sheet2')
        writer.save()
        self.output.i_insert("Consolidations done.")

    def ground_report(self):
        """
        runs consolidations report on entire warehouse
        :return: None (Outputs report to output console)
        """
        self.output.r_insert("")
        vals = [*self.area_dict.values()]
        vals.sort(key=lambda x: x.aisle)
        for i in vals:
            temp_con = ground_con(i, self.controller.bay_range, self.controller.gap, self.controller.hp)
            self.output.i_insert("Aisle {} has {} consolidations\n".format(i.aisle, len(temp_con)))
            self.output.update()

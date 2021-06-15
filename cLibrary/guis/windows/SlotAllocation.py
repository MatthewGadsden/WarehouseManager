import datetime
import pandas as pd
from cLibrary.guis.windows.WidgetWindow import *
from cLibrary.methods.AreaMethods import dayxhits_sort_1_4, best_sort_1_4
from cLibrary.widgets.WinOutput import WinOutput


class SlotAllocation(WidgetWindow):

    def __init__(self, master, controller):
        """
        initialise from super
        :param master: master window / frame
        :param controller: program controller
        """
        super(SlotAllocation, self).__init__(master, controller)
        self.areas = controller.areas
        self.area_dict = {}
        self.file_path = None

        for area in self.areas.values():
            self.area_dict[area.area_name] = area

        self.combo_options = [key for key in self.area_dict]

        self.start_val = StringVar(self)
        self.start_val.set(list(self.areas.values())[0].area_name)

        self.start_val2 = StringVar(self)
        self.start_val2.set(list(self.areas.values())[0].area_name)

        # create sort areas widgets
        bg = Label(self)
        sort_area = Frame(self)
        sort_area.place(x=60, y=70, width=210, height=100)
        sort_area.grid_rowconfigure((0, 1, 2), weight=2)
        sort_area.grid_columnconfigure(1, weight=1)
        sort_area.grid_columnconfigure(0, weight=1)
        if True:
            title = Label(sort_area, text="Best Ave Hits Sort", bg="cornflower blue", font="bold 10")
            title.grid(row=0, column=0, columnspan=2, sticky=NSEW)
            combo_title = Label(sort_area, text="Area", bg="light grey", font="bold 10")
            combo_title.grid(row=1, column=0, sticky=NSEW)
            sort_button = Button(sort_area, text="Sort", relief="groove", bg="maroon1", font="bold 10",
                                 command=lambda: self.sort_area(self.area_dict[self.start_val.get()], best_sort_1_4))
            sort_button.grid(row=1, column=1, sticky=NSEW)
            self.combo = Combobox(sort_area, values=self.combo_options, textvariable=self.start_val,
                             font="bold 10", state="readonly")
            self.combo.grid(row=2, column=0, sticky=NSEW)
            open_button = Button(sort_area, text="Open", relief="groove", bg="chartreuse2", font="bold 10",
                                 command=lambda: self.open_file())
            open_button.grid(row=2, column=1, sticky=NSEW)
            pass
        sort_area.update()
        bg.place(x=sort_area.winfo_x()-2, y=sort_area.winfo_y()-2, width=sort_area.winfo_width()+4, height=sort_area.winfo_height()+4)

        # create sort2 areas widgets
        bg3 = Label(self)
        sort_area2 = Frame(self)
        sort_area2.place(x=60, y=180, width=210, height=100)
        sort_area2.grid_rowconfigure((0, 1, 2), weight=2)
        sort_area2.grid_columnconfigure(1, weight=1)
        sort_area2.grid_columnconfigure(0, weight=1)
        if True:
            title = Label(sort_area2, text="Day x Hits Sort", bg="cornflower blue", font="bold 10")
            title.grid(row=0, column=0, columnspan=2, sticky=NSEW)
            combo_title = Label(sort_area2, text="Area", bg="light grey", font="bold 10")
            combo_title.grid(row=1, column=0, sticky=NSEW)
            sort_button = Button(sort_area2, text="Sort", relief="groove", bg="maroon1", font="bold 10",
                                 command=lambda: self.sort_area(self.area_dict[self.start_val2.get()], dayxhits_sort_1_4))
            sort_button.grid(row=1, column=1, sticky=NSEW)
            self.combo2 = Combobox(sort_area2, values=self.combo_options, textvariable=self.start_val2,
                                  font="bold 10", state="readonly")
            self.combo2.grid(row=2, column=0, sticky=NSEW)
            open_button = Button(sort_area2, text="Open", relief="groove", bg="chartreuse2", font="bold 10",
                                 command=lambda: self.open_file())
            open_button.grid(row=2, column=1, sticky=NSEW)
            pass
        sort_area2.update()
        bg3.place(x=sort_area2.winfo_x() - 2, y=sort_area2.winfo_y() - 2, width=sort_area2.winfo_width() + 4,
                 height=sort_area2.winfo_height() + 4)

        # create warehouse report widgets
        bg2 = Label(self)
        warehouse_reports = Frame(self)
        warehouse_reports.place(x=sort_area.winfo_x(), y=sort_area.winfo_y()+sort_area.winfo_height()+120,
                                width=sort_area.winfo_width(), height=90)
        warehouse_reports.grid_columnconfigure(0, weight=1)
        warehouse_reports.grid_rowconfigure(0, weight=1)
        warehouse_reports.grid_rowconfigure(1, weight=2)
        if True:
            title = Label(warehouse_reports, text="Get Warehouse Report", bg="cornflower blue", font="bold 10")
            title.grid(row=0, column=0, sticky=NSEW)

            sort_button = Button(warehouse_reports, text="Print Report", relief="groove", bg="maroon1",
                                 command=lambda: self.warehouse_report(dayxhits_sort_1_4), font="bold 10")
            sort_button.grid(row=1, column=0, sticky=NSEW)
            pass
        warehouse_reports.update()
        bg2.place(x=warehouse_reports.winfo_x()-2,
                  y=warehouse_reports.winfo_y()-2,
                  width=warehouse_reports.winfo_width() + 4,
                  height=warehouse_reports.winfo_height() + 4)

        self.output = WinOutput(self, width=870, height=self.controller.wig_height - 80,
                                x=self.controller.wig_width - 870 - 20, y=70,
                                wrap=WORD, bg="snow", font="none 10", relief="groove")

    def sort_area(self, area, sort):
        """
        Run slot allocation, and create excel doc
        :param area: warehouse area to run on
        :param sort: sort type to use
        :return: None
        """
        now = datetime.datetime.now()
        date = "{0}-{1}-{2}".format(now.day, now.month, now.year)
        self.output.r_insert("Sorting " + area.area_name + " now...\n")
        self.output.update()
        area_sort = sort(area)
        self.file_path = "resources/output/"+area.area_name + "_{}_sorted.xlsx".format(date)
        for i, switch in enumerate(area_sort):
            area_sort[i] = [switch[0].spot_id,
                            (str(switch[0].item.item_id) if switch[0].item is not None else str(switch[0].item)),
                            "", switch[1].spot_id,
                            (str(switch[1].item.item_id) if switch[1].item is not None else str(switch[1].item)), ""]

        df = pd.DataFrame(area_sort, columns=["From Slot", "Item Code", "Moved?", "To Slot", "Item Code", "Moved?"])

        writer = pd.ExcelWriter(self.file_path)
        df.to_excel(writer, 'Sheet1')
        writer.save()
        self.output.i_insert(area.area_name.title() + " has been sorted.")
        self.output.update()

    def warehouse_report(self, sort):
        """
        run warehouse report for slot allocation
        :param sort: sort to use
        :return: None (output prints to the Output console)
        """
        area_nums = []
        self.output.r_insert("")
        for area in self.areas.values():
            self.output.i_insert(" " + str(area.area_name.title()) + " has " + str(len(sort(area))) + " swaps to make\n")
            self.output.update()

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

    def load_title(self, text="Slot Allocation Program", bg="burlywood1", relief="groove"):
        """
        load window title
        :return: None
        """
        super(SlotAllocation, self).load_title(text=text, bg=bg, relief=relief)
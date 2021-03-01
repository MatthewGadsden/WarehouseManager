from tkinter import *
from tkinter.font import *
from tkinter.ttk import Combobox, Progressbar, Notebook, Separator
from cLibrary.methods.general import *

from cLibrary.widgets.controlPanel.DashGrid import DashGrid
from cLibrary.widgets.AppIcon import AppIcon
from cLibrary.widgets.Clock import Clock
from cLibrary.widgets.DayNightButton import DayNightButton

from cLibrary.guis.popups.ErrorWindow import ErrorWindow
from cLibrary.guis.popups.DashDimensions import DashDimensions
from cLibrary.guis.popups.AreasPopUp import AreasPopUp
from cLibrary.guis.popups.ChooseNewWarehouse import ChooseNewWarehouse
from cLibrary.guis.popups.ImportCategories import ImportCategories
from cLibrary.guis.popups.SelectArea import SelectArea

from cLibrary.guis.windows.SlotAllocation import SlotAllocation
from cLibrary.guis.windows.MGCons import MGCons
from cLibrary.guis.windows.Relay import Relay
from cLibrary.guis.windows.DistroWindow import Distro

from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename
from PIL import ImageTk, Image
from cLibrary.structure.warehouse.Warehouse import Warehouse
from cLibrary.structure.warehouse.CustomArea import CustomArea
from cLibrary.methods.AreaMethods import best_sort_1_4
from cLibrary.guis.Controller import Controller
import shutil


class MGSlotSystem(Tk):
    def __init__(self, item_file, slot_file, stock_file, hits_file):
        """
        initialize the MGSlotSystem Window
        :param item_file: item data of warehouse
        :param slot_file: slot data of warehouse
        :param stock_file: stock data of warehouse
        :param hits_file: hit data of warehouse
        """
        super().__init__()
        # values
        self.slot_file = slot_file
        self.item_file = item_file
        self.stock_file = stock_file
        self.hits_file = hits_file

        # window properties
        error_check = True
        while error_check:
            try:
                self.warehouse = Warehouse(item_file, slot_file, stock_file, hits_file)
                error_check = not error_check
            except Exception as error:
                self.wait_window(ErrorWindow(self, error))

        self.recent_cps = []
        self.load_recent_cps()

        self.configure(width=1200, height=650, bg="snow")
        self.controller = Controller(self, self.warehouse)
        self.resizable(False, False)
        self.title("MGSS")
        self.iconbitmap("resources/img/main-icon.ico")
        self.grab_set()

        self.root_menu = Menu(self)
        self.menus()
        self.config(menu=self.root_menu)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.dash = DashGrid(self.controller.container, self.controller)
        self.load_cp()
        self.task_bar()

    def on_close(self, event=None):
        """
        MGSS system close procedure
        :param event: catch event if needed
        :return: None
        """
        self.save_cp()
        self.save_recent_cps()
        self.save_con_settings()
        self.controller.on_close()
        wigs_w = self.controller.wigs_w
        wigs_h = self.controller.wigs_h
        x = self.winfo_x()
        y = self.winfo_y()
        with open("resources/data/config.txt", "w") as file:
            file.write("{},{}\n{},{}".format(wigs_w, wigs_h, x, y))
        self.destroy()

    def update_dash(self):
        """
        reset dash board of control panel
        :return: None
        """
        self.dash.destroy()
        self.save_cp()
        self.dash = DashGrid(self.controller.container, self.controller)
        self.load_cp()

    def menus(self):
        """
        Create the menu bar for MGSS
        :return: None
        """
        # FILE MENUS
        file_menu = Menu(self.root_menu, tearoff=0)
        self.root_menu.add_cascade(label="File", menu=file_menu)

        if True:
            file_menu.add_command(label="New Warehouse...", accelerator="Ctrl+N", command=lambda: ChooseNewWarehouse(self))
            new_menu = Menu(file_menu, tearoff=0)
            file_menu.add_cascade(label="New...", menu=new_menu)
            new_menu.add_command(label="Item File", command=lambda: self.change_warehouse(item_file=askopenfilename()))
            new_menu.add_command(label="Slot File", command=lambda: self.change_warehouse(slot_file=askopenfilename()))
            new_menu.add_command(label="ItmSlot File",
                                 command=lambda: self.change_warehouse(stock_file=askopenfilename()))
            new_menu.add_command(label="Hits File", command=lambda: self.change_warehouse(hits_file=askopenfilename()))

        file_menu.add_separator()

        # File Commands
        if True:    # File Commands
            file_menu.add_command(label="Save...", accelerator="Ctrl+S", command=lambda:self.save_ware_format())
            # file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=lambda:self.save_as())
            file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=lambda:self.load_ware_format())

            self.bind_all("<Control-s>", self.save_ware_format)
            self.bind_all("<Control-S>", self.save_ware_format)
            # self.bind_all("<Control-Shift-S>", self.save_as)
            # self.bind_all("<Control-Shift-s>", self.save_as)
            self.bind_all("<Control-O>", self.load_ware_format)
            self.bind_all("<Control-o>", self.load_ware_format)
        # Open Recent
        if True:    # Open Recent
            open_recent_menu = Menu(file_menu,tearoff=0)
            file_menu.add_cascade(label="Open Recent...", menu=open_recent_menu)

        # File Commands
        if True:    # File Commands

            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.on_close)

        # EDIT MENUS
        if True:
            edit_menu = Menu(self.root_menu, tearoff=0)
            self.root_menu.add_cascade(label="Edit", menu=edit_menu)
            edit_menu.add_command(label="Warehouse Areas", command=lambda: AreasPopUp(self, self.controller))
            edit_menu.add_command(label="Categories")
            pass

        # VIEW MENUS
        if True:
            view_menu = Menu(self.root_menu, tearoff=0)
            self.root_menu.add_cascade(label="View", menu=view_menu)

            # control panel cascade
            if True:
                control_panel = Menu(view_menu, tearoff=0)
                view_menu.add_cascade(label="Control Panel", menu=control_panel)

                control_panel.add_command(label="Save CP", command=lambda: self.menu_save_cp())
                control_panel.add_command(label="Load CP", command=lambda: self.menu_load_cp())

                self.recent_cps_menu = Menu(control_panel, tearoff=0)
                control_panel.add_cascade(label="Load Recent CP...", menu=self.recent_cps_menu)

                for recent in self.recent_cps:
                    self.recent_cps_menu.add_command(label=re.sub(r'.*/', '/', recent),
                                                     command=lambda e=recent: self.menu_load_cp(e))
                control_panel.add_command(label="Dimensions", command=lambda: DashDimensions(self, self.controller))
            view_menu.add_separator()
            view_menu.add_command(label="Warehouse",
                                  command=lambda: SelectArea(self,
                                                             self.warehouse,
                                                             False))

        # STOCK MENUS
        if True:
            stock_menu = Menu(self.root_menu, tearoff=0)
            self.root_menu.add_cascade(label="Stock", menu=stock_menu)

            # Stock.Import Menus
            if True:  # File.Import Menus
                stock_import_menu = Menu(stock_menu,
                                         tearoff=0)
                stock_menu.add_cascade(label="Import",
                                       menu=stock_import_menu)
                stock_import_menu.add_cascade(label="New Stock (Unavailable)")
                stock_import_menu.add_cascade(label="Stock Categories",
                                              command=lambda: ImportCategories(self,
                                                                               controller=self.controller,
                                                                               width=500,
                                                                               height=175,
                                                                               title="Import Categories",)
                                              )

        # HELP MENUS
        help_menu = Menu(self.root_menu, tearoff=0)
        self.root_menu.add_cascade(label="Help", menu=help_menu)

    def task_bar(self):
        """
        Load task bar apps and widgets
        :return: None
        """
        osa = AppIcon(self, SlotAllocation, img="resources/img/mgsa-icon.ico", name="Slot Allocation", bg="#FFB642")  # Slot allocation app button
        osa.place(x=97, y=0)

        osa2 = AppIcon(self, MGCons, img="resources/img/cons-icon.ico", name="Consolidations", bg="#FFFFFF")  # Consolidations app button
        osa2.place(x=37, y=0)

        osa3 = AppIcon(self, Relay, img="resources/img/relay-icon.ico", name="Warehouse Relay", bg="#b37fc1",)  # Relay warehouse app button
        osa3.place(x=67, y=0)

        osa4 = AppIcon(self, Distro, img="resources/img/distro-icon.ico", name="Distro", bg="#FFB642")
        osa4.place(x=7, y=0)

        clock = Clock(self, height=25)  # Clock Widget
        clock.place(x=self.winfo_width() - 50, y=0)

    def change_warehouse(self, item_file=None, slot_file=None, stock_file=None, hits_file=None):
        """
        Load new warehouse to the system
        :param item_file: item data
        :param slot_file: slot data
        :param stock_file: stock data
        :param hits_file: hits data
        :return: None
        """
        if item_file == '' or slot_file == '' or stock_file == '' or hits_file == '':
            return None
        if slot_file is None:
            slot_file = self.slot_file
        else:
            self.slot_file = slot_file
        if item_file is None:
            item_file = self.item_file
        else:
            self.item_file = item_file
        if stock_file is None:
            stock_file = self.stock_file
        else:
            self.stock_file = stock_file
        if hits_file is None:
            hits_file = self.hits_file
        else:
            self.hits_file = hits_file

        self.warehouse = Warehouse(item_file, slot_file, stock_file, hits_file)
        self.controller.warehouse = self.warehouse
        self.controller.save_areas()
        self.controller.load_areas()
        self.save_cp()
        self.load_cp()

    def daynight(self, night):
        """
        Toggle dark mode
        :param night: checking if dark mode is active
        :return: None
        """
        if night:
            self.configure(bg="gray26")
            for child in self.winfo_children():
                child.configure(bg="gray26")

            for child in self.controller.container.winfo_children():
                child.configure(bg="gray26")
                for child2 in child.winfo_children():
                    child2.configure(bg="gray38")
        else:
            self.configure(bg="snow")
            for child in self.winfo_children():
                child.configure(bg="snow")

            for child in self.controller.container.winfo_children():
                child.configure(bg="snow")
                for child2 in child.winfo_children():
                    child2.configure(bg="gray78")

    def save_ware_format(self, event=None):
        """
        Save warehouse layout
        :param event: event catch
        :return: None
        """
        file_dir = asksaveasfilename(initialdir="resources/data/saves", filetypes=(('wf files', '*.wf'),), defaultextension=".wf")
        if file_dir == '':
            return None
        with open(file_dir, "w") as file:
            for area in self.controller.areas:
                file.write(area.area_name)
                for spot in area:
                    file.write("," + spot.spot_id)
                file.write("\n")

    def load_ware_format(self, event=None, file=None):
        """
        Load warehouse format from file
        :param event: catch event
        :param file: file to load
        :return: None
        """
        if file is None:
            file_dir = askopenfilename(initialdir="resources/data/saves", filetypes=(('wf files', '*.wf'),))
        else:
            file_dir = file
        if file_dir == '':
            return None
        with open(file_dir, "r") as file:
            areas = []
            for line in file:
                line = line.strip("\n").split(",")
                i = 1
                while i < len(line):
                    try:
                        save_line = line[i]
                        spot = self.controller.warehouse.find_area(line[i])
                        if spot is None:
                            raise ValueError("Save File Error:\n\nSpot ID {} was found in save file, contact help is further "
                                             "assistance is needed".format(save_line))
                        line[i] = spot
                    except Exception as e:
                        line.pop(i)
                        ErrorWindow(self, e)
                        i -= 1
                    i += 1
                try:
                    areas.append(CustomArea(line[1:], line[0], self.warehouse))
                except Exception as e:
                    ErrorWindow(self, "Error creating area {}\n\nThis area has been removed".format(line[0]))
        self.controller.areas = areas

    def save_con_settings(self, event=None):
        """
        Save Consolidation settings
        :param event: event catch
        :return: None
        """
        with open("resources/data/con-set.txt", "w") as file:
            file.write(str(self.controller.bay_range) + "," + str(self.controller.gap) + "," + str(self.controller.hp))
            file.close()

    def menu_load_cp(self, file=None):
        """
        loading control panel save file
        :param file: file to load to the control panel
        :return: None
        """
        if file is None:
            file_dir = askopenfilename(initialdir="resources/data/saves", filetypes = (('cp files', '*.cp'),))
        else:
            file_dir = file
            file_dir = re.sub(r'.*resources', 'resources', file_dir)
        if file_dir == '':
            return None
        self.add_recent_cp(file_dir)
        file = open(file_dir, "r")
        ws = []
        for line in file:
            ws.append(line.strip("\n"))

        i = 0
        for widget in self.dash:
            widget.clean()
            if i < len(ws) and ws[i] != "None":
                widget.load_widget(ws[i])
            i += 1
        file.close()

    def menu_save_cp(self):
        """
        save current control panel layout
        :return: None
        """
        file_dir = asksaveasfilename(initialdir="resources/data/saves", filetypes=(('cp files', '*.cp'),), defaultextension=".cp")
        if file_dir == '':
            return None
        file = open(file_dir, "w")
        f_line = True
        for widget in self.dash:
            if f_line:
                of_type = str(widget.current_widget_type)
                f_line = False
            else:
                of_type = "\n" + str(widget.current_widget_type)
            file.write(of_type)
        file.close()

    def load_recent_cps(self):
        """
        Load in recent control panel files
        :return: None
        """
        with open("resources/data/recent_cps.txt", "r") as file:
            for line in file:
                self.recent_cps.append(line.strip("\n"))

    def save_recent_cps(self):
        """
        Save recent control panel files for next load of system
        :return: None
        """
        with open("resources/data/recent_cps.txt", "w") as file:
            f_line = True
            for line in self.recent_cps:
                if f_line:
                    file.write(line)
                    f_line = False
                else:
                    file.write("\n" + line)

    def save_cp(self):
        """
        Save current control panel layout to default control panel file location
        :return: None
        """
        with open("resources/data/widgets.cp", "w") as file:
            f_line = True
            for widget in self.dash:
                if f_line:
                    of_type = str(widget.current_widget_type)
                    f_line = False
                else:
                    of_type = "\n" + str(widget.current_widget_type)
                file.write(of_type)

    def load_cp(self, file_dir=None):
        """
        Load control panel layout from file, if file_dir == None load default file
        :param file_dir: file location to load from
        :return: None
        """
        with open("resources/data/widgets.cp", "r") if file_dir is None else open(file_dir, "r") as file:
            ws = []
            for line in file:
                ws.append(line.strip("\n"))

            i = 0
            for widget in self.dash:
                widget.clean()
                if i < len(ws) and ws[i] != "None":
                    widget.load_widget(ws[i])
                i += 1

    def add_recent_cp(self, file_dir):
        """
        Add control panel save file to recent cp files
        :param file_dir: file to add
        :return: None
        """
        while len(self.recent_cps) > 9:
            self.recent_cps.pop(len(self.recent_cps)-1)
            self.recent_cps_menu.delete(len(self.recent_cps)-1)
        i = 0
        while i < len(self.recent_cps):
            if self.recent_cps[i] == file_dir:
                self.recent_cps.pop(i)
                self.recent_cps_menu.delete(i)
                break
            i += 1
        self.recent_cps.insert(0, file_dir)
        self.recent_cps_menu.insert(0, label=re.sub(r'.*/', '/', file_dir), command=lambda e=file_dir: self.menu_load_cp(e), itemType=COMMAND)

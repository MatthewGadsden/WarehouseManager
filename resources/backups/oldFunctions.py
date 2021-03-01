# from tkinter import *
#
# def best_slots(self, number, used_slots):
#     max_i = self.get_filled_pick_slots_count()
#     if number > max_i:
#         number = max_i
#
#     i = 0
#     bestList = []
#     while i < number:
#         best = None
#         for spot in self:
#             if best is None:
#                 best = spot.get_best_avehitsday_aux(bestList, used_slots)
#             else:
#                 temp = spot.get_best_avehitsday_aux(bestList, used_slots)
#                 if temp is None:
#                     pass
#                 elif temp.get_item_avehitsday() > best.get_item_avehitsday():
#                     best = temp
#         if best is not None:
#             bestList.append(best)
#         i += 1
#
#     for object in bestList:
#         print(object.item.avehitsday, end=" ")
#     print()
#     return bestList
#
#
# def sort_area():
#     title = Label(sort_area, text="Sort Area", bg="cornflower blue")
#     title.grid(row=0, column=0, columnspan=2, sticky=NSEW)
#     combo_title = Label(sort_area, text="Area", bg="light grey")
#     combo_title.grid(row=1, column=0, sticky=NSEW)
#     sort_button = Button(sort_area, text="Sort", relief="groove", bg="maroon1",
#                          command=lambda: self.sort_area(self.area_dict[self.start_val.get()]))
#     sort_button.grid(row=1, column=1, sticky=NSEW)
#     combo = Combobox(sort_area, values=[key for key in self.area_dict], textvariable=self.start_val)
#     combo.grid(row=2, column=0)
#     open_button = Button(sort_area, text="Open", relief="groove", bg="chartreuse2",
#                          command=lambda: self.open_file())
#     open_button.grid(row=2, column=1, sticky=NSEW)
#
# def backup_sort_1_4(area, method):
#     if not isinstance(area, Area):
#         raise TypeError("area must be of type Area")
#
#     levels = []
#     for i in range(1, 5):
#         l = area.create_level(i)
#         levels.append(l)
#
#     pri_two = levels[0] + levels[3]
#     for slot in pri_two:
#         print(slot.spot_id)
#     pri_one = levels[1] + levels[2]
#
#     bsn = len(pri_one)
#     wsn = len(pri_two)
#     sn = bsn + wsn
#
#     bs = method(area, sn)
#
#     ws = bs[bsn:]
#     bs = bs[:bsn]
#
#     empties = []
#     for slot in pri_one:
#         if slot.item is None:
#             empties.append(slot)
#
#     moving_slots = []
#     for slot in bs:
#         if slot.level == (1 or 4):
#             moving_slots.append(slot)
#
#     moving_slots2 = []
#     for slot in ws:
#         if slot.level == (2 or 3):
#             if slot.item.carton.weight < 9000:
#                 moving_slots2.append(slot)
#
#     moving_slots2 += empties
#     if len(moving_slots2) < len(moving_slots):
#         moving_slots = moving_slots[:len(moving_slots2)]
#     else:
#         moving_slots2 = moving_slots2[:len(moving_slots)]
#
#     radix_sort_slots(moving_slots)
#     radix_sort_slots(moving_slots2)
#     moving_list = []
#     for i in range(len(moving_slots)):
#         moving_list.append((moving_slots[i], moving_slots2[i]))
#     return moving_list
#
# def sorted_1_4(area, method):
#     if not isinstance(area, Area):
#         raise TypeError("area must be of type Area")
#
#     levels = []
#     for i in range(1, 5):
#         l = area.create_level(i)
#         levels.append(l)
#
#     pri_two = levels[0] + levels[3]
#     pri_one = levels[1] + levels[2]
#
#     bsn = len(pri_one)
#     wsn = len(pri_two)
#     sn = bsn + wsn
#
#     bs = method(area, sn)
#     bs += area.get_empty_slots()
#
#     ws = bs[bsn:]
#     bs = bs[:bsn]
#
#     i = 0
#     while i < len(bs) or i < len(ws):
#         if i < len(bs) and (bs[i].level == "2" or bs[i].level == "3"):
#             bs.pop(i)
#             i -= 1
#         elif i < len(ws) and (ws[i].level == "1" or ws[i].level == "4"):
#             ws.pop(i)
#             i -= 1
#         i += 1
#
#     radix_sort_slots(ws)
#     radix_sort_slots(bs)
#
#     moving_list = []
#     for i in range(len(bs)):
#         moving_list.append((bs[i], ws[i]))
#     return moving_list

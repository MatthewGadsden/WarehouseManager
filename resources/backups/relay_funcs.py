# def new_relay(category, area, excess_area, controller, outfile):
#     cat_items = category.get_items()  # Category Items List
#     area_spots = area.get_pick_slots()  # Area Location List
#     excess_spots = excess_area.get_empty_slots()  # Excess Location List
#
#     aisles = {}  # Aisles Dictionary
#     for spot in area_spots:
#         if aisles.get(spot.aisle) is None:
#             aisles[spot.aisle] = [spot, ]
#         else:
#             aisles[spot.aisle].append(spot)
#
#     for aisle_key in aisles.keys():
#         if (ord(aisle_key[0]) % 2) == 0:
#             aisles[aisle_key].sort(key=lambda x: x.pick_slot, reverse=True)
#             aisles[aisle_key].sort(key=lambda x: x.bay, reverse=True)
#         else:
#             aisles[aisle_key].sort(key=lambda x: x.pick_slot, reverse=False)
#             aisles[aisle_key].sort(key=lambda x: x.bay, reverse=False)
#
#     excess_items = []
#     for pickslot in [inner for outer in aisles.values() for inner in outer]:
#         if not (pickslot.item in cat_items) and pickslot.item is not None:
#             excess_items.append(pickslot.item)
#
#     assert len(cat_items) < len(area_spots), "There are more items in the category than spots in the Area selected"
#     assert len(excess_items) < len(excess_spots), "Not enough free excess spots to clear the area"
#
#     items_small = [item for item in cat_items if item.get_unit_vol() < 0.0014]
#     items_medium = [item for item in cat_items if 0.007 >= item.get_unit_vol() >= 0.0014]
#     items_large = [item for item in cat_items if item.get_unit_vol() > 0.007]
#
#     items_small.sort(key=lambda item: item.avehitsday)
#     items_medium.sort(key=lambda item: item.avehitsday)
#     items_large.sort(key=lambda item: item.avehitsday)
#
#     count_large = len(items_large)
#     count_medium = len(items_medium)
#     count_small = len(items_small)
#
#     count_spare_spots = len(area_spots) - len(cat_items)
#     count_small = count_small + round((count_small / len(cat_items)) * count_spare_spots)
#     count_medium = count_medium + round((count_medium / len(cat_items)) * count_spare_spots)
#     count_large = len(area_spots) - count_small - count_medium
#
#     # Create levels 2+3 (priority levels)
#     levels_23 = []
#     levels_14 = []
#     for aisle in aisles.values():
#         levels_23.append(create_level(aisle, ("2", "3")))
#         levels_14.append(create_level(aisle, ("1", "4")))
#
#     levels_14.sort(key=lambda x: x[0].aisle, reverse=True)
#     levels_23.sort(key=lambda x: x[0].aisle, reverse=True)
#
#     levels_14 = flatten_list_of_lists(levels_14)
#     levels_23 = flatten_list_of_lists(levels_23)
#
#     spots_large = levels_14[:math.floor(count_large/2)]+levels_23[:math.ceil(count_large/2)]
#     spots_medium = levels_14[math.floor(count_large/2):math.floor(count_large/2)+math.floor(count_medium/2)] + levels_23[math.ceil(count_large/2):math.ceil(count_large/2)+math.ceil(count_medium/2)]
#     spots_small = levels_14[math.floor(count_large/2)+math.floor(count_medium/2):] + levels_23[math.ceil(count_large/2)+math.ceil(count_medium/2):]
#
#     sheet1 = []
#     for i, item in enumerate(items_large):
#         sheet1.append([item.pick_slot.spot_id if item.pick_slot is not None else "No Location", item.item_id, item.pick_slot.qty if item.pick_slot is not None else "0", "", spots_large[i].spot_id, ""])
#     for i, item in enumerate(items_medium):
#         sheet1.append([item.pick_slot.spot_id if item.pick_slot is not None else "No Location", item.item_id, item.pick_slot.qty if item.pick_slot is not None else "0", "", spots_medium[i].spot_id, ""])
#     for i, item in enumerate(items_small):
#         sheet1.append([item.pick_slot.spot_id if item.pick_slot is not None else "No Location", item.item_id, item.pick_slot.qty if item.pick_slot is not None else "0", "", spots_small[i].spot_id, ""])
#
#     sheet2 = []
#     for i, item in enumerate(excess_items):
#         sheet2.append([item.pick_slot.spot_id, item.item_id, item.pick_slot.qty, "", excess_spots[i].spot_id, ""])
#
#     df1 = pd.DataFrame(sheet1, columns=['Current Location', 'Item ID', 'Qty', 'Qty Check', 'New Location', 'Moved Check'])
#     df2 = pd.DataFrame(sheet2, columns=['Current Location', 'Item ID', 'Qty', 'Qty Check', 'New Location', 'Moved Check'])
#     writer = pd.ExcelWriter(outfile)
#     df1.to_excel(writer, 'Sheet1')
#     df2.to_excel(writer, 'Sheet2')
#     writer.save()
#     return outfile

# WORK IN PROGRESS
# def relay_cat_by_size(area, category, excess_area, controller, outfile):
#     """
#     Relays items in a category into a certain area of the warehouse
#     :param area: Area to relay category in
#     :param category: Category of items to relay
#     :param excess_area: Where excess items go (if they don't fit in area)
#     :param controller: Program controller
#     :param outfile: file to export to
#     :return: the file the output was sent to.
#     """
#     og_area = area
#     area = copy.deepcopy(area)
#
#     og_excess = excess_area
#     excess_area = copy.deepcopy(excess_area)
#
#     og_cat = category
#     category = copy.deepcopy(category)
#
#     if not isinstance(area, Area):
#         raise TypeError("Type error in arguments of relay_cat_by_size")
#     area_slots = area.get_pick_slots()
#     excess_slots = excess_area.get_pick_slots()
#     items = category.get_items()
#
#     area_slots.sort(key=lambda x: x.spot_id)
#     excess_slots.sort(key=lambda x: x.spot_id)
#
#     aisles = []
#     current_aisle = None
#     temp_aisle = []
#
#     for spot in area_slots:
#         if spot.aisle != current_aisle:
#             current_aisle = spot.aisle
#             temp_aisle = [spot]
#             aisles.append(temp_aisle)
#         else:
#             temp_aisle.append(spot)
#
#     current_aisle = None
#     for spot in excess_slots:
#         if spot.aisle != current_aisle:
#             current_aisle = spot.aisle
#             temp_aisle = [spot]
#             aisles.append(temp_aisle)
#         else:
#             temp_aisle.append(spot)
#
#     for aisle in aisles:
#         aisle.sort(key=lambda x: x.spot_id, reverse=True) if aisle[0].aisle % 2 == 0 else aisle.sort(key=lambda x: x.spot_id, reverse=False)
#
#     spots = [spot for sublist in aisles for spot in sublist]
#
#     small = [item for item in items if item.get_unit_vol() < 0.0014]
#     medium = [item for item in items if 0.007 >= item.get_unit_vol() >= 0.0014]
#     large = [item for item in items if item.get_unit_vol() > 0.007]
#
#     small.sort(key=lambda x: x.get_unit_vol(), reverse=True)
#     medium.sort(key=lambda x: x.get_unit_vol(), reverse=True)
#     large.sort(key=lambda x: x.get_unit_vol(), reverse=True)
#
#     from cLibrary.structure.warehouse.CustomArea import CustomArea
#
#     l_area = CustomArea(spots[:len(large)], 'large')
#     m_area = CustomArea(spots[len(large):len(large)+len(medium)], 'medium')
#     s_area = CustomArea(spots[len(large)+len(medium):len(large)+len(medium)+len(small)], 'small')
#
#     l_area = copy.deepcopy(l_area)
#     m_area = copy.deepcopy(m_area)
#     s_area = copy.deepcopy(s_area)
#
#     l_area_slots = l_area.get_pick_slots()
#     m_area_slots = m_area.get_pick_slots()
#     s_area_slots = s_area.get_pick_slots()
#
#     # move template = ['current location', 'item code', 'qty', 'qty check', 'new location', 'moved?']
#     moves = {}
#     for i, item in enumerate(large):
#         if item.pick_slot:
#             moves[l_area_slots[i].spot_id] = item.pick_slot.spot_id
#             l_area_slots[i].switch_item_slot(item)
#
#     for i, item in enumerate(medium):
#         if item.pick_slot:
#             moves[m_area_slots[i].spot_id] = item.pick_slot.spot_id
#             m_area_slots[i].switch_item_slot(item)
#
#     for i, item in enumerate(small):
#         if item.pick_slot:
#             moves[s_area_slots[i].spot_id] = item.pick_slot.spot_id
#             s_area_slots[i].switch_item_slot(item)
#
#     best_moves = best_sort_1_4(s_area) + best_sort_1_4(m_area) + best_sort_1_4(l_area)
#     best_moves = dict([(y.spot_id, x.spot_id) for [x, y] in best_moves if y.item is not None] + [(x.spot_id, y.spot_id) for [x, y] in best_moves if x.item is not None])
#
#     end_moves = {}
#     for key in moves:
#         m = best_moves.get(key)
#         end_moves[moves[key]] = (m if m is not None else key)
#
#     data = [['Current Location', 'Item Code', 'Qty', 'Qty Check', 'New Location', 'Moved?']]
#     for (x, y) in end_moves.items():
#         pickslot = controller.warehouse.get_pickslot(x)
#         item_id = pickslot.item.item_id if pickslot.item is not None else None
#         data.append([x, item_id, pickslot.qty, '', y, ''])
#
#     outfile = (outfile + '.csv' if outfile[-4:] != '.csv' else outfile)
#     with open(outfile, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerows(data)
#
#     return outfile

#
# def sorted_3241(area, method):
#     area_spots = area.get_pick_slots()  # Area Location List
#     cat_items = [i.item for i in area.get_filled_pick_slots()]
#
#     aisles = {}  # Aisles Dictionary
#     for spot in area_spots:
#         if aisles.get(spot.aisle) is None:
#             aisles[spot.aisle] = [spot, ]
#         else:
#             aisles[spot.aisle].append(spot)
#
#     for aisle_key in aisles.keys():
#         if (ord(aisle_key[0]) % 2) == 0:
#             aisles[aisle_key].sort(key=lambda x: x.pick_slot, reverse=True)
#             aisles[aisle_key].sort(key=lambda x: x.bay, reverse=True)
#         else:
#             aisles[aisle_key].sort(key=lambda x: x.pick_slot, reverse=False)
#             aisles[aisle_key].sort(key=lambda x: x.bay, reverse=False)
#
#     items_small = [item for item in cat_items if item.get_unit_vol() < 0.0014]
#     items_medium = [item for item in cat_items if 0.007 >= item.get_unit_vol() >= 0.0014]
#     items_large = [item for item in cat_items if item.get_unit_vol() > 0.007]
#
#     items_small.sort(key=lambda item: item.avehitsday, reverse=True)
#     items_medium.sort(key=lambda item: item.avehitsday, reverse=True)
#     items_large.sort(key=lambda item: item.avehitsday, reverse=True)
#
#     count_small = len(items_small)
#     count_medium = len(items_medium)
#     count_large = len(items_large)
#     count_total = count_small + count_large + count_medium
#
#     small_ratio = count_small / count_total
#     medium_ratio = count_medium / count_total
#     large_ratio = count_large / count_total
#
#     lvl_1 = create_size_level_lists(aisles, 1, small_ratio, medium_ratio, large_ratio)
#     lvl_2 = create_size_level_lists(aisles, 2, small_ratio, medium_ratio, large_ratio)
#     lvl_3 = create_size_level_lists(aisles, 3, small_ratio, medium_ratio, large_ratio)
#     lvl_4 = create_size_level_lists(aisles, 4, small_ratio, medium_ratio, large_ratio)
#
#     small = [lvl_3[2], lvl_2[2], lvl_4[2], lvl_1[2]]
#     medium = [lvl_3[1], lvl_2[1], lvl_4[1], lvl_1[1]]
#     large = [lvl_3[0], lvl_2[0], lvl_4[0], lvl_1[0]]
#
#     count = 0
#     for lvl in large:
#         for i, item in enumerate(items_large[count: len(lvl)]):
#             if item.pick_slot in lvl:
#                 items_large.remove(item)
#                 lvl.remove(item.pick_slot)
#         count += len(lvl)
#
#     count = 0
#     for lvl in medium:
#         for i, item in enumerate(items_medium[count: len(lvl)]):
#             if item.pick_slot in lvl:
#                 items_medium.remove(item)
#                 lvl.remove(item.pick_slot)
#         count += len(lvl)
#
#     count = 0
#     for lvl in small:
#         for i, item in enumerate(items_small[count: len(lvl)]):
#             if item.pick_slot in lvl:
#                 items_small.remove(item)
#                 lvl.remove(item.pick_slot)
#         count += len(lvl)
#
#     moves = []
#     count = 0
#     for lvl in large:
#         for i, item in enumerate(items_large[count: len(lvl)]):
#             moves.append((item.pick_slot, lvl[i]))
#         count += len(lvl)
#
#     count = 0
#     for lvl in medium:
#         for i, item in enumerate(items_medium[count: len(lvl)]):
#             moves.append((item.pick_slot, lvl[i]))
#         count += len(lvl)
#
#     count = 0
#     for lvl in small:
#         for i, item in enumerate(items_small[count: len(lvl)]):
#             moves.append((item.pick_slot, lvl[i]))
#         count += len(lvl)
#
#     return moves

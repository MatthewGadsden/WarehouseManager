from cLibrary.structure.item.Item import Item


class CatList:

    def __init__(self):
        self.categories = {}

    def add_category(self, category):
        if category in self:
            pass
        else:
            self[category] = Category(category)

    def add_item(self, item, category):
        if not isinstance(item, Item):
            raise TypeError("Cannot add non-item to a Category")
        if category in self:
            self[category].add_item(item)
        else:
            self[category] = Category(category)
            self[category].add_item(item)

    def values(self):
        return self.categories.values()

    def keys(self):
        return self.categories.keys()

    def __contains__(self, item):
        return item in self.categories.keys()

    def __setitem__(self, key, value):
        self.categories[key] = value

    def __iter__(self):
        return self.categories.__iter__()

    def __getitem__(self, key):
        return self.categories[key]

    def __len__(self):
        return len(self.categories)


class Category:

    def __init__(self, name):
        self.name = name
        self.count = 0
        self.items = {}

    def add_item(self, item):
        self[item.item_id] = item

    def get_items(self):
        return list(self.items.values())

    def __contains__(self, item_id):
        return item_id in self.items.keys()

    def pop(self, key):
        self.items.pop(key)

    def values(self):
        return self.items.values()

    def keys(self):
        return self.items.keys()

    def __setitem__(self, item_id, item):
        if self.items.get(item_id) is None:
            self.count += 1
        self.items[item_id] = item

    def __iter__(self):
        return self.items.__iter__()

    def __getitem__(self, item_id):
        return self.items[item_id]

    def __len__(self):
        return self.count

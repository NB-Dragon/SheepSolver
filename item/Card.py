class Card(object):
    def __init__(self, origin_data):
        self._origin_data = self.generate_format_data_item(origin_data)
        self._parent_note = set()
        self._children_node = set()

    @staticmethod
    def generate_format_data_item(origin_data):
        level = int(origin_data["id"].split("-")[0])
        card_type = origin_data["type"]
        min_x, max_x = origin_data["rolNum"], origin_data["rolNum"] + 8
        min_y, max_y = origin_data["rowNum"], origin_data["rowNum"] + 8
        return {"level": level, "type": card_type, "min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}

    def get_card_level(self):
        return self._origin_data["level"]

    def get_card_type(self):
        return self._origin_data["type"]

    def clac_area(self):
        width = self._origin_data["max_x"] - self._origin_data["min_x"]
        height = self._origin_data["max_y"] - self._origin_data["min_y"]
        return width * height

    def get_position(self):
        return [self._origin_data["min_x"], self._origin_data["min_y"],
                self._origin_data["max_x"], self._origin_data["max_y"]]

    def clac_iou(self, card):
        current_position = self.get_position()
        other_position = card.get_position()
        min_x = max(current_position[0], other_position[0])
        min_y = max(current_position[1], other_position[1])
        max_x = min(current_position[2], other_position[2])
        max_y = min(current_position[3], other_position[3])
        overlap_area = max(0, max_x - min_x) * max(0, max_y - min_y)
        current_area = self.clac_area()
        other_area = card.clac_area()
        return overlap_area / (current_area + other_area - overlap_area)

    def has_parent(self):
        return len(self._parent_note) > 0

    def get_children_set(self):
        return self._children_node

    def add_parent(self, card_index):
        self._parent_note.add(card_index)

    def recover_parent(self, card_index):
        self._parent_note.remove(card_index)

    def add_children(self, card_index):
        self._children_node.add(card_index)

    def recover_children(self, card_index):
        self._children_node.remove(card_index)

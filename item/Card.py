#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
class Card(object):
    def __init__(self, origin_data):
        self._origin_data = self.generate_format_data_item(origin_data)
        self._parent_note = set()
        self._children_node = set()

    @staticmethod
    def generate_format_data_item(origin_data):
        card_id = origin_data["id"]
        card_type = origin_data["type"]
        min_x, max_x = origin_data["rolNum"], origin_data["rolNum"] + 8
        min_y, max_y = origin_data["rowNum"], origin_data["rowNum"] + 8
        return {"id": card_id, "type": card_type, "min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}

    def get_card_id(self):
        return self._origin_data["id"]

    def get_card_level(self):
        return int(self._origin_data["id"].split("-")[0])

    def get_card_type(self):
        return self._origin_data["type"]

    def clac_area(self):
        width = self._origin_data["max_x"] - self._origin_data["min_x"]
        height = self._origin_data["max_y"] - self._origin_data["min_y"]
        return width * height

    def get_position(self):
        return [self._origin_data["min_x"], self._origin_data["min_y"],
                self._origin_data["max_x"], self._origin_data["max_y"]]

    def has_parent(self):
        return len(self._parent_note) > 0

    def get_children_set(self):
        return self._children_node

    def add_parent(self, card_index):
        self._parent_note.add(card_index)

    def remove_parent(self, card_index):
        self._parent_note.remove(card_index)

    def add_children(self, card_index):
        self._children_node.add(card_index)

    def remove_children(self, card_index):
        self._children_node.remove(card_index)

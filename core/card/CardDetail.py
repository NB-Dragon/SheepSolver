#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/31 00:00
# Create User: NB-Dragon
class CardDetail(object):
    def __init__(self, origin_data):
        self._generate_card_attribute(origin_data)
        self._parent_note = set()
        self._children_node = set()

    def _generate_card_attribute(self, origin_data):
        self._attribute = dict()
        self._attribute["id"] = origin_data["id"]
        self._attribute["type"] = origin_data["type"]
        self._attribute["level"] = int(origin_data["id"].split("-")[0])
        self._attribute["min_x"] = origin_data["rolNum"]
        self._attribute["min_y"] = origin_data["rowNum"]
        self._attribute["max_x"] = origin_data["rolNum"] + 8
        self._attribute["max_y"] = origin_data["rowNum"] + 8

    def reset_card_position(self, min_x, min_y):
        self._attribute["min_x"] = min_x
        self._attribute["min_y"] = min_y
        self._attribute["max_x"] = min_x + 8
        self._attribute["max_y"] = min_y + 8
        self._parent_note.clear()
        self._children_node.clear()

    def get_card_id(self):
        return self._attribute["id"]

    def get_card_type(self):
        return self._attribute["type"]

    def get_card_level(self):
        return self._attribute["level"]

    def get_card_area(self):
        width = self._attribute["max_x"] - self._attribute["min_x"]
        height = self._attribute["max_y"] - self._attribute["min_y"]
        return width * height

    def get_card_position(self):
        return [self._attribute["min_x"], self._attribute["min_y"], self._attribute["max_x"], self._attribute["max_y"]]

    def add_parent(self, card_index):
        self._parent_note.add(card_index)

    def remove_parent(self, card_index):
        self._parent_note.remove(card_index)

    def add_children(self, card_index):
        self._children_node.add(card_index)

    def remove_children(self, card_index):
        self._children_node.remove(card_index)

    def is_card_freedom(self):
        return len(self._parent_note) == 0

    def get_children_set(self):
        return self._children_node

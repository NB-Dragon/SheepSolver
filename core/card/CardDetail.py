#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/31 00:00
# Create User: NB-Dragon
class CardDetail(object):
    def __init__(self):
        self._card_id = None
        self._card_type = None
        self._card_level = None
        self._card_position = None

        self._parent_node = set()
        self._children_node = set()

    def recognize_origin_map_data(self, origin_data):
        self._card_id = origin_data["id"]
        self._card_type = origin_data["type"]
        self._card_level = int(origin_data["id"].split("-")[0])
        min_x, min_y = origin_data["rolNum"], origin_data["rowNum"]
        self._card_position = [min_x, min_y, min_x + 8, min_y + 8]

    def export_compute_data(self):
        result_dict = dict()
        result_dict["card_id"] = self._card_id
        result_dict["card_type"] = self._card_type
        result_dict["card_level"] = self._card_level
        result_dict["card_position"] = self._card_position
        result_dict["parent_node"] = list(self._parent_node)
        result_dict["children_node"] = list(self._children_node)
        return result_dict

    def import_compute_data(self, compute_data):
        self._card_id = compute_data["card_id"]
        self._card_type = compute_data["card_type"]
        self._card_level = compute_data["card_level"]
        self._card_position = compute_data["card_position"]
        self._parent_node = set(compute_data["parent_node"])
        self._children_node = set(compute_data["children_node"])

    def get_card_id(self):
        return self._card_id

    def get_card_type(self):
        return self._card_type

    def get_card_level(self):
        return self._card_level

    def get_card_position(self):
        return self._card_position

    def get_parent_node(self):
        return self._parent_node

    def get_children_node(self):
        return self._children_node

    def get_card_area(self):
        width = self._card_position[2] - self._card_position[0]
        height = self._card_position[3] - self._card_position[1]
        return width * height

    def add_parent(self, card_index):
        self._parent_node.add(card_index)

    def remove_parent(self, card_index):
        self._parent_node.remove(card_index)

    def add_children(self, card_index):
        self._children_node.add(card_index)

    def remove_children(self, card_index):
        self._children_node.remove(card_index)

    def clear_all_relation(self):
        self._parent_node.clear()
        self._children_node.clear()

    def is_card_no_parent(self):
        return len(self._parent_node) == 0

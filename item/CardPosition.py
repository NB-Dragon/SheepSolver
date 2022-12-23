#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import random


class CardPosition(object):
    def __init__(self, sort_mode):
        # 当前抽牌的选择方式
        self._sort_mode = sort_mode
        # 以序号注册所有卡牌数据
        self._origin_data = {}
        # 以序号注册可操作卡牌数据
        self._head_data = {}
        # 当前登记的序号
        self._card_count = 0

    def append_level_card(self, card_list):
        start_index = len(self._origin_data)
        self._append_origin_data(card_list)
        end_index = len(self._origin_data)
        new_card_data = {key: self._origin_data[key] for key in range(start_index, end_index)}
        self._handle_overlap_data(new_card_data)

    def generate_head_data(self):
        for key_index, card_detail in self._origin_data.items():
            if not card_detail.has_parent():
                self._head_data[key_index] = card_detail

    def get_head_description(self):
        return "-".join([str(item) for item in sorted(self._head_data.keys())])

    def get_card_detail(self, card_index):
        return self._origin_data[card_index]

    def pick_card(self, card_index):
        card_detail = self._origin_data[card_index]
        children_set = card_detail.get_children_set()
        self._head_data.pop(card_index)
        for children_key in children_set:
            children_item = self._origin_data[children_key]
            children_item.remove_parent(card_index)
            if not children_item.has_parent():
                self._head_data[children_key] = children_item

    def recover_card(self, card_index):
        card_detail = self._origin_data[card_index]
        children_set = card_detail.get_children_set()
        self._head_data[card_index] = card_detail
        for children_key in children_set:
            children_item = self._origin_data[children_key]
            children_item.add_parent(card_index)
            if children_key in self._head_data:
                self._head_data.pop(children_key)

    def get_head_key_list(self):
        if self._sort_mode == "normal":
            return list(self._head_data.keys())
        elif self._sort_mode == "random":
            origin_list = list(self._head_data.keys())
            random.shuffle(origin_list)
            return origin_list
        elif self._sort_mode == "reverse":
            return sorted(self._head_data.keys(), reverse=True)
        elif self._sort_mode == "top-first":
            sorted_dict = dict(sorted(self._head_data.items(), key=lambda a: a[1].get_card_level(), reverse=True))
            return list(sorted_dict.keys())
        else:
            return []

    def is_head_data_empty(self):
        return len(self._head_data.keys()) == 0

    def _append_origin_data(self, card_list):
        for card_item in card_list:
            self._origin_data[self._card_count] = card_item
            self._card_count += 1

    def _handle_overlap_data(self, card_dict):
        old_card_dict = {key: self._origin_data[key] for key in self._origin_data.keys() if key not in card_dict}
        for key_new, card_new in card_dict.items():
            for key_old, card_old in old_card_dict.items():
                if self._clac_iou(card_new, card_old) > 0:
                    card_new.add_children(key_old)
                    card_old.add_parent(key_new)

    @staticmethod
    def _clac_iou(new_card, old_card):
        new_card_position = new_card.get_position()
        old_card_position = old_card.get_position()
        min_x = max(new_card_position[0], old_card_position[0])
        min_y = max(new_card_position[1], old_card_position[1])
        max_x = min(new_card_position[2], old_card_position[2])
        max_y = min(new_card_position[3], old_card_position[3])
        overlap_area = max(0, max_x - min_x) * max(0, max_y - min_y)
        new_card_area = new_card.clac_area()
        old_card_area = old_card.clac_area()
        return overlap_area / (new_card_area + old_card_area - overlap_area)

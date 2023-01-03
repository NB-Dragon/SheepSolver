#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/31 00:00
# Create User: NB-Dragon
import random


class OperationPool(object):
    def __init__(self, card_container, sort_mode):
        self._card_container = card_container
        self._sort_mode = sort_mode
        # 以序号注册可操作卡牌数据
        self._head_list = []

    def generate_head_list(self):
        self._head_list = self._card_container.get_freedom_card_list()

    def generate_head_description(self):
        return "-".join([str(item) for item in sorted(self._head_list)])

    def is_game_over(self):
        return len(self._head_list) == 0

    def pick_card(self, card_index):
        card_detail = self._card_container.get_card_detail(card_index)
        children_set = card_detail.get_children_set()
        self._head_list.remove(card_index)
        for children_key in children_set:
            children_item = self._card_container.get_card_detail(children_key)
            children_item.remove_parent(card_index)
            if children_item.is_card_freedom():
                self._head_list.append(children_key)

    def recover_card(self, card_index):
        card_detail = self._card_container.get_card_detail(card_index)
        children_set = card_detail.get_children_set()
        self._head_list.append(card_index)
        for children_key in children_set:
            children_item = self._card_container.get_card_detail(children_key)
            children_item.add_parent(card_index)
            if children_key in self._head_list:
                self._head_list.remove(children_key)

    def get_head_key_list(self):
        if self._sort_mode == "normal":
            return list(self._head_list)
        elif self._sort_mode == "reverse":
            return sorted(self._head_list, reverse=True)
        elif self._sort_mode == "top-first":
            origin_card_level_dict = self._get_card_level_dict()
            sorted_dict = dict(sorted(origin_card_level_dict.items(), key=lambda a: a[1], reverse=True))
            return list(sorted_dict.keys())
        elif self._sort_mode == "random":
            result_list = list(self._head_list)
            random.shuffle(result_list)
            return result_list
        else:
            return []

    def _get_card_level_dict(self):
        result_dict = dict()
        for card_index in self._head_list:
            card_detail = self._card_container.get_card_detail(card_index)
            result_dict[card_index] = card_detail.get_card_level()
        return result_dict

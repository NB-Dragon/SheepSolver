#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/31 00:00
# Create User: NB-Dragon
import random


class OperationPool(object):
    def __init__(self, card_container):
        self._card_container = card_container
        # 以序号注册可操作卡牌数据
        self._head_list = []

    def generate_head_list(self):
        self._head_list = self._card_container.get_freedom_card_list()

    def generate_head_description(self):
        return "-".join([str(item) for item in sorted(self._head_list)])

    def is_game_over(self):
        normal_key_list = self._get_normal_key_list("normal")
        return len(normal_key_list) == 0

    def get_head_key_list(self, solve_type):
        return self._get_normal_key_list(solve_type)

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

    def _get_normal_key_list(self, solve_type):
        if solve_type == "normal":
            return list(self._head_list)
        elif solve_type == "index":
            return sorted(self._head_list)
        elif solve_type == "index-reverse":
            return sorted(self._head_list, reverse=True)
        elif solve_type == "level-bottom":
            return sorted(self._head_list, key=self._sort_for_level)
        elif solve_type == "level-top":
            return sorted(self._head_list, key=self._sort_for_level, reverse=True)
        elif solve_type == "random":
            result_list = list(self._head_list)
            random.shuffle(result_list)
            return result_list
        else:
            return []

    def _sort_for_level(self, card_index):
        card_detail = self._card_container.get_card_detail(card_index)
        return card_detail.get_card_level()

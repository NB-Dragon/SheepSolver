#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/31 00:00
# Create User: NB-Dragon
import random


class OperationPool(object):
    def __init__(self, card_container):
        self._card_container = card_container
        # 以序号注册可操作卡牌数据
        self._main_zone = []

    def prepare_game_data(self):
        self._main_zone = self._card_container.get_main_zone_card_list()

    def get_main_zone_show_card_list(self, solve_type):
        if solve_type == "normal":
            return list(self._main_zone)
        elif solve_type == "index":
            return sorted(self._main_zone)
        elif solve_type == "index-reverse":
            return sorted(self._main_zone, reverse=True)
        elif solve_type == "level-bottom":
            return sorted(self._main_zone, key=self._sort_for_level)
        elif solve_type == "level-top":
            return sorted(self._main_zone, key=self._sort_for_level, reverse=True)
        elif solve_type == "random":
            result_list = list(self._main_zone)
            random.shuffle(result_list)
            return result_list
        else:
            return []

    def pick_card(self, card_index):
        self._pick_card_normal(card_index)

    def recover_card(self, card_index):
        self._recover_card_normal(card_index)

    def _pick_card_normal(self, card_index):
        self._main_zone.remove(card_index)
        children_card_list = self._query_children_node(card_index)
        children_card_dict = self._card_container.get_card_detail_dict(children_card_list)
        self._remove_parent_for_each_children(children_card_dict, card_index)
        self._show_card_for_each_children(children_card_dict)

    def _recover_card_normal(self, card_index):
        self._main_zone.append(card_index)
        children_card_list = self._query_children_node(card_index)
        children_card_dict = self._card_container.get_card_detail_dict(children_card_list)
        self._add_parent_for_each_children(children_card_dict, card_index)
        self._hide_card_for_each_children(children_card_dict)

    def _query_children_node(self, card_index):
        card_detail = self._card_container.get_card_detail_item(card_index)
        return card_detail.get_children_node()

    @staticmethod
    def _add_parent_for_each_children(children_dict, parent_index):
        for card_index, card_detail in children_dict.items():
            card_detail.add_parent(parent_index)

    @staticmethod
    def _remove_parent_for_each_children(children_dict, parent_index):
        for card_index, card_detail in children_dict.items():
            card_detail.remove_parent(parent_index)

    def _show_card_for_each_children(self, children_dict):
        for card_index, card_detail in children_dict.items():
            if card_detail.is_card_no_parent():
                self._main_zone.append(card_index)

    def _hide_card_for_each_children(self, children_dict):
        for card_index, card_detail in children_dict.items():
            if card_index in self._main_zone:
                self._main_zone.remove(card_index)

    def _sort_for_level(self, card_index):
        card_detail = self._card_container.get_card_detail_item(card_index)
        return card_detail.get_card_level()

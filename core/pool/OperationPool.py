#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/31 00:00
# Create User: NB-Dragon
import random


class OperationPool(object):
    def __init__(self, card_container):
        self._card_container = card_container
        self._card_sequence = None
        # 以序号注册可操作卡牌数据
        self._main_zone = []
        # 在准备阶段对所有卡牌排序
        self._sort_card = dict()

    def prepare_game_data(self, card_sequence):
        self._card_sequence = card_sequence
        self._main_zone = self._card_container.get_main_zone_card_list()
        self._sort_card = self._generate_default_sorted_dict()

    def get_main_zone_show_card_list(self, algorithm):
        if algorithm in self._sort_card:
            result_list = [item for item in self._sort_card[algorithm] if item in self._main_zone]
            return result_list
        elif algorithm == "normal":
            return list(self._main_zone)
        elif algorithm == "random":
            result_list = list(self._main_zone)
            random.shuffle(result_list)
            return result_list
        else:
            return []

    def pick_card(self, card_index):
        self._pick_card_normal(card_index)
        self._card_sequence_pick_card(card_index)

    def recover_card(self, card_index):
        self._recover_card_normal(card_index)
        self._card_sequence_recover_card()

    def _pick_card_normal(self, card_index):
        children_card_list = self._query_children_node(card_index)
        children_card_dict = self._card_container.get_card_detail_dict(children_card_list)
        self._remove_parent_for_each_children(children_card_dict, card_index)
        self._adjust_main_zone_for_pick_card(children_card_dict, card_index)

    def _recover_card_normal(self, card_index):
        children_card_list = self._query_children_node(card_index)
        children_card_dict = self._card_container.get_card_detail_dict(children_card_list)
        self._add_parent_for_each_children(children_card_dict, card_index)
        self._adjust_main_zone_for_recover_card(children_card_dict, card_index)

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

    def _adjust_main_zone_for_pick_card(self, children_dict, card_index):
        self._pick_main_zone_card(card_index)
        children_dict = self._filter_for_no_parent(children_dict)
        self._main_zone.extend(children_dict.keys())

    def _adjust_main_zone_for_recover_card(self, children_dict, card_index):
        self._recover_main_zone_card(card_index)
        children_dict = self._filter_for_main_zone(children_dict, self._main_zone)
        [self._main_zone.remove(card_index) for card_index in children_dict.keys()]

    def _pick_main_zone_card(self, card_index):
        self._main_zone.remove(card_index)

    def _recover_main_zone_card(self, card_index):
        self._main_zone.append(card_index)

    def _card_sequence_pick_card(self, card_index):
        card_detail = self._card_container.get_card_detail_item(card_index)
        card_type = card_detail.get_card_type()
        self._card_sequence.append_card_item(card_index, card_type)

    def _card_sequence_recover_card(self):
        self._card_sequence.remove_last_item()

    @staticmethod
    def _filter_for_no_parent(sorted_card_data):
        result_dict = dict()
        for card_index, card_detail in sorted_card_data.items():
            if card_detail.is_card_no_parent():
                result_dict[card_index] = card_detail
        return result_dict

    @staticmethod
    def _filter_for_main_zone(sorted_card_data, origin_list):
        result_dict = dict()
        for card_index, card_detail in sorted_card_data.items():
            if card_index in origin_list:
                result_dict[card_index] = card_detail
        return result_dict

    def _generate_default_sorted_dict(self):
        result_dict = dict()
        card_index_list = range(self._card_container.get_card_count())
        result_dict["index-ascending"] = list(sorted(card_index_list, key=self._sort_for_index))
        result_dict["index-descending"] = list(sorted(card_index_list, key=self._sort_for_index, reverse=True))
        result_dict["level-bottom"] = list(sorted(card_index_list, key=self._sort_for_level))
        result_dict["level-top"] = list(sorted(card_index_list, key=self._sort_for_level, reverse=True))
        return result_dict

    # noinspection PyMethodMayBeStatic
    def _sort_for_index(self, card_index):
        return card_index

    def _sort_for_level(self, card_index):
        card_detail = self._card_container.get_card_detail_item(card_index)
        return card_detail.get_card_level()

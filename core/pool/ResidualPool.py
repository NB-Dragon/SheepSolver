#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/31 00:00
# Create User: NB-Dragon
class ResidualPool(object):
    def __init__(self, card_container):
        self._card_container = card_container
        # 当前操作池有多少张卡牌
        self._pool_count = 0
        # 当前操作池可容纳的最大牌数
        self._pool_limit = 7
        # 当前操作池卡牌类别及序号
        self._pool_card = []
        # 已经成功消除的卡牌信息
        self._disappear_card = []

    def is_card_type_close_to_limit(self):
        return len(self._pool_card) == self._pool_limit - 1

    def is_pool_count_close_to_limit(self):
        return self._pool_count == self._pool_limit - 1

    def is_card_type_close_to_possible(self):
        return len(self._pool_card) == self._pool_limit - 2

    def get_all_card_type_list(self):
        return [item["card_type"] for item in self._pool_card]

    def get_almost_card_type_list(self):
        return [item["card_type"] for item in self._pool_card if len(item["card_list"]) == 2]

    def get_sorted_card_type_list(self):
        sorted_pool_card = sorted(self._pool_card, key=lambda a: len(a["card_list"]), reverse=True)
        return [item["card_type"] for item in sorted_pool_card]

    def pick_card(self, card_index):
        card_detail = self._card_container.get_card_detail(card_index)
        card_pair = self._find_match_card_pair(card_detail)
        if card_pair is None:
            card_pair = self._create_new_card_pair(card_detail)
        card_pair["card_list"].append(card_index)
        self._pool_count += 1
        self._card_disappear_for_same(card_pair)

    def recover_card(self, card_index):
        card_detail = self._card_container.get_card_detail(card_index)
        card_pair = self._find_match_card_pair(card_detail)
        if card_pair is None:
            card_pair = self._create_old_card_pair(card_index)
            self._pool_count += 3
        card_pair["card_list"].remove(card_index)
        self._pool_count -= 1
        self._card_disappear_for_back(card_pair)

    def _card_disappear_for_same(self, card_pair):
        if len(card_pair["card_list"]) == 3:
            disappear_item = self._create_disappear_item(card_pair)
            self._disappear_card.append(disappear_item)
            self._pool_card.remove(card_pair)
            self._pool_count -= 3

    def _card_disappear_for_back(self, card_pair):
        if len(card_pair["card_list"]) == 0:
            self._pool_card.remove(card_pair)

    def _create_disappear_item(self, card_pair):
        pair_index = self._pool_card.index(card_pair)
        return {"pair_index": pair_index, "card_pair": card_pair}

    def _create_new_card_pair(self, card_detail):
        card_type = card_detail.get_card_type()
        card_pair = {"card_type": card_type, "card_list": []}
        self._pool_card.append(card_pair)
        return card_pair

    def _create_old_card_pair(self, card_detail):
        disappear_item = self._disappear_card.pop(-1)
        pair_index, card_pair = disappear_item["pair_index"], disappear_item["card_pair"]
        self._pool_card.insert(pair_index, card_pair)
        return card_pair

    def _find_match_card_pair(self, card_detail):
        card_type = card_detail.get_card_type()
        for pair_item in self._pool_card:
            if pair_item["card_type"] == card_type:
                return pair_item
        return None

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon


class ResidualPool(object):
    def __init__(self, project_helper):
        self._project_helper = project_helper
        self._card_type_name = self._generate_card_type_name()
        # 当前操作池有多少张卡牌
        self._pool_count = 0
        # 当前操作池可容纳的最大牌数
        self._pool_limit = 7
        # 当前操作池帕牌类别及数量
        self._pool_card = {}

    def get_pool_detail(self):
        return self._pool_card

    def is_pool_count_close_to_limit(self):
        return self._pool_count == 6

    def is_card_type_close_to_limit(self):
        return len(self._pool_card.keys()) == self._pool_limit - 1

    def is_card_type_close_to_possible(self):
        return len(self._pool_card.keys()) == self._pool_limit - 2

    def get_pool_state(self):
        result_text = ""
        for card_type, card_count in self._pool_card.items():
            result_text += self._card_type_name[card_type] * card_count
        return result_text

    def pick_card(self, card_detail):
        self._pool_count += 1
        card_type = card_detail.get_card_type()
        if card_type in self._pool_card:
            self._pool_card[card_type] += 1
        else:
            self._pool_card[card_type] = 1
        self._make_card_disappear(card_type)

    def recover_card(self, card_detail):
        card_type = card_detail.get_card_type()
        if card_type in self._pool_card:
            if self._pool_card[card_type] == 1:
                self._pool_card.pop(card_type)
            else:
                self._pool_card[card_type] -= 1
            self._pool_count -= 1
        else:
            self._pool_card[card_type] = 2
            self._pool_count += 2

    def _make_card_disappear(self, card_type):
        if self._pool_card[card_type] == 3:
            self._pool_count -= 3
            self._pool_card.pop(card_type)

    def _generate_card_type_name(self):
        global_config = self._project_helper.get_project_config()["global"]
        return global_config["type_name"]

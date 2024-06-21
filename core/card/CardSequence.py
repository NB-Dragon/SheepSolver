#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2024/06/20 00:00
# Create User: NB-Dragon
class CardSequence(object):
    def __init__(self):
        self._index_list = []
        self._type_list = []

    def append_card_item(self, card_index, card_data):
        self._index_list.append(card_index)
        self._type_list.append((card_index, card_data))

    def remove_last_item(self):
        self._index_list.pop(-1)
        self._type_list.pop(-1)

    def get_pick_index_list(self):
        return list(self._index_list)

    def get_pick_type_list(self):
        return list(self._type_list)

    def clear_all_sequence(self):
        self._index_list.clear()
        self._type_list.clear()

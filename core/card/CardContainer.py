#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/31 00:00
# Create User: NB-Dragon
import json
from core.card.CardDetail import CardDetail


class CardContainer(object):
    def __init__(self):
        # 以序号注册所有卡牌数据
        self._card_dict = {}

    def append_level_card(self, level_card_data):
        self._append_origin_data(level_card_data)
        self._handle_overlap_data(level_card_data)

    def export_compute_data_string(self):
        result_dict = {key: value.export_compute_data() for key, value in self._card_dict.items()}
        return json.dumps(result_dict)

    def import_compute_data_string(self, data_string):
        self._card_dict.clear()
        import_data = json.loads(data_string)
        for index, value in import_data.items():
            card_detail = CardDetail()
            card_detail.import_compute_data(value)
            self._card_dict[int(index)] = card_detail

    def get_main_zone_card_list(self):
        result_list = list()
        for card_index, card_detail in self._card_dict.items():
            if card_detail.is_card_no_parent():
                result_list.append(card_index)
        return result_list

    def get_card_count(self):
        return len(self._card_dict)

    def get_card_detail_item(self, card_index):
        return self._card_dict[card_index]

    def get_card_detail_dict(self, card_list):
        result_dict = dict()
        for card_index in card_list:
            result_dict[card_index] = self._card_dict[card_index]
        return result_dict

    def _append_origin_data(self, level_card_data):
        current_index = self.get_card_count()
        for level_card_item in level_card_data:
            card_detail = self._create_card_detail(level_card_item)
            self._card_dict[current_index] = card_detail
            current_index += 1

    def _handle_overlap_data(self, level_card_data):
        new_card_dict = self._generate_new_card_dict(len(level_card_data))
        old_card_dict = self._generate_old_card_dict(len(level_card_data))
        for new_card_key, new_card_value in new_card_dict.items():
            for old_card_key, old_card_value in old_card_dict.items():
                if self._clac_iou(new_card_value, old_card_value) > 0:
                    new_card_value.add_children(old_card_key)
                    old_card_value.add_parent(new_card_key)

    def _generate_new_card_dict(self, new_card_count):
        new_card_key_list = self._get_new_card_key_list(new_card_count)
        return {card_index: self._card_dict[card_index] for card_index in new_card_key_list}

    def _generate_old_card_dict(self, new_card_count):
        old_card_key_list = self._get_old_card_key_list(new_card_count)
        return {card_index: self._card_dict[card_index] for card_index in old_card_key_list}

    def _get_new_card_key_list(self, new_card_count):
        current_card_count = self.get_card_count()
        begin_index = current_card_count - new_card_count
        return [item for item in range(begin_index, current_card_count)]

    def _get_old_card_key_list(self, new_card_count):
        current_card_count = self.get_card_count()
        end_index = current_card_count - new_card_count
        return [item for item in range(0, end_index)]

    @staticmethod
    def _create_card_detail(origin_data):
        card_detail = CardDetail()
        card_detail.recognize_origin_map_data(origin_data)
        return card_detail

    @staticmethod
    def _clac_iou(new_card, old_card):
        new_card_position = new_card.get_card_position()
        old_card_position = old_card.get_card_position()
        min_x = max(new_card_position[0], old_card_position[0])
        min_y = max(new_card_position[1], old_card_position[1])
        max_x = min(new_card_position[2], old_card_position[2])
        max_y = min(new_card_position[3], old_card_position[3])
        overlap_area = max(0, max_x - min_x) * max(0, max_y - min_y)
        new_card_area = new_card.get_card_area()
        old_card_area = old_card.get_card_area()
        return overlap_area / (new_card_area + old_card_area - overlap_area)

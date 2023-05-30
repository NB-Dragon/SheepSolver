#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import os
from core.data.ShuffleHelper import ShuffleHelper
from helper.FileHelper import FileHelper


class StaticDataGenerator(object):
    def __init__(self, static_map_path):
        self._static_map_path = static_map_path
        self._shuffle_helper = None

    def generate_final_map_file(self, summary_data: dict, save_path):
        if summary_data["err_code"] == 0:
            map_hash = self._get_game_map_hash(summary_data)
            map_seed = self._get_game_map_seed(summary_data)
            map_real_data = self._generate_shuffle_map_data(map_hash, map_seed)
            self._handle_save_file(save_path, map_real_data)

    def _generate_shuffle_map_data(self, map_hash, map_seed_dict):
        origin_map_data = self._load_map_cache_data(map_hash)
        self._shuffle_helper = ShuffleHelper(map_seed_dict["map_seed"])
        if isinstance(origin_map_data, dict):
            origin_map_data.update(map_seed_dict)
            self._ensure_map_key_sorted(origin_map_data)
            self._reset_map_card_type(origin_map_data)
        return origin_map_data

    def _load_map_cache_data(self, map_hash):
        map_cache_file = self._generate_map_cache_path(map_hash)
        return FileHelper().read_json_data(map_cache_file)

    def _generate_map_cache_path(self, map_hash):
        map_cache_name = "{}.json".format(map_hash)
        return os.path.join(self._static_map_path, map_cache_name)

    def _ensure_map_key_sorted(self, map_struct_data):
        self._adjust_data_dict(map_struct_data, "blockTypeData")
        self._adjust_data_dict(map_struct_data, "levelData")

    def _reset_map_card_type(self, map_struct_data):
        type_list = self._generate_shuffle_list(map_struct_data)
        card_list = self._generate_card_list(map_struct_data)
        card_list = [item for item in card_list if item["type"] == 0]
        for card_item, card_type in zip(card_list, type_list):
            card_item["type"] = card_type

    def _generate_shuffle_list(self, map_struct_data):
        result_list = []
        for key, count in map_struct_data["blockTypeData"].items():
            result_list.extend([int(key)] * count * 3)
        self._shuffle_helper.shuffle(result_list, len(result_list))
        return list(reversed(result_list))

    @staticmethod
    def _generate_card_list(map_struct_data):
        result_list = []
        for level_index, level_data in map_struct_data["levelData"].items():
            result_list.extend(level_data)
        return result_list

    @staticmethod
    def _adjust_data_dict(data_dict, sort_key):
        data_dict[sort_key] = dict(sorted(data_dict[sort_key].items(), key=lambda item: int(item[0])))

    @staticmethod
    def _get_game_map_hash(summary_data):
        return summary_data["data"]["map_md5"][1]

    @staticmethod
    def _get_game_map_seed(summary_data):
        result_dict = dict()
        result_dict["map_seed"] = summary_data["data"]["map_seed"]
        result_dict["map_seed_2"] = summary_data["data"]["map_seed_2"]
        return result_dict

    @staticmethod
    def _handle_save_file(save_path, map_data):
        if isinstance(map_data, dict):
            FileHelper().write_json_data(save_path, map_data)
            print("=====> 当前游戏的地图数据生成成功")
        else:
            print("=====> 当前游戏的地图数据生成失败")
            print("=====> 请根据文档指引申请进群，私信群主获取解决方案")

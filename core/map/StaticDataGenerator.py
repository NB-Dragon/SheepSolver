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

    def generate_final_map_file(self, summary_data: dict, save_path):
        if summary_data["err_code"] == 0:
            map_hash = self._get_game_map_hash(summary_data)
            map_seed = self._get_game_map_seed(summary_data)
            map_real_data = self._generate_shuffle_map_data(map_hash, map_seed)
            self._handle_save_file(map_real_data, save_path)

    def _generate_shuffle_map_data(self, map_hash, map_seed_dict):
        origin_map_data = self._load_map_cache_data(map_hash)
        if isinstance(origin_map_data, dict):
            self._ensure_map_key_sorted(origin_map_data)
            block_type_data, shuffle_seed = origin_map_data["blockTypeData"], map_seed_dict["map_seed"]
            type_list = self._generate_shuffle_list(block_type_data, shuffle_seed)
            self._reset_map_data_type(type_list, origin_map_data)
            origin_map_data.update(map_seed_dict)
        return origin_map_data

    def _load_map_cache_data(self, map_hash):
        map_cache_file = self._generate_map_cache_path(map_hash)
        return FileHelper().read_json_data(map_cache_file)

    def _generate_map_cache_path(self, map_hash):
        map_cache_name = "{}.json".format(map_hash)
        return os.path.join(self._static_map_path, map_cache_name)

    @staticmethod
    def _ensure_map_key_sorted(map_cache_data):
        block_type_data = map_cache_data["blockTypeData"]
        map_cache_data["blockTypeData"] = dict(sorted(block_type_data.items(), key=lambda item: int(item[0])))
        level_data = map_cache_data["levelData"]
        map_cache_data["levelData"] = dict(sorted(level_data.items(), key=lambda item: int(item[0])))

    @staticmethod
    def _generate_shuffle_list(block_type_data, map_seed):
        result_list = []
        for key, count in block_type_data.items():
            result_list.extend([int(key)] * count * 3)
        ShuffleHelper(map_seed).shuffle(result_list)
        return result_list

    @staticmethod
    def _generate_card_list(origin_map_data):
        result_list = []
        for level_index, level_data in origin_map_data["levelData"].items():
            result_list.extend(level_data)
        return result_list

    def _reset_map_data_type(self, type_list, origin_map_data):
        card_list = self._generate_card_list(origin_map_data)
        card_list = [item for item in card_list if item["type"] == 0]
        for card_item, card_type in zip(card_list, type_list):
            card_item["type"] = card_type

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
    def _handle_save_file(map_real_data, save_path):
        if isinstance(map_real_data, dict):
            FileHelper().write_json_data(save_path, map_real_data)
            print("=====> 当前游戏的地图数据生成成功")
        else:
            print("=====> 当前游戏的地图数据生成失败")
            print("=====> 众筹计划: 每日手动重制地图数据; 加入Q群\"331240392\"了解详情")

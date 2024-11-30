#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import os
from core.data.ShuffleHelper import ShuffleHelper
from helper.FileHelper import FileHelper


class StaticDataGenerator(object):
    def __init__(self, project_helper):
        self._project_helper = project_helper
        self._shuffle_helper = None
        self._prepare_runtime_param()

    def _prepare_runtime_param(self):
        self._save_file_path = self._project_helper.get_global_online_data()
        self._static_map_path = self._project_helper.get_project_path("static_map")

    def fill_seed_data_into_cache(self, map_struct, map_seed):
        self._map_struct_fill_data(map_struct, map_seed)

    def fill_seed_data_into_file(self, map_hash, map_seed):
        map_struct_file = self._generate_map_struct_file_path(map_hash)
        if not os.path.exists(map_struct_file):
            print("=====> 游戏地图数据生成失败")
            print("=====> 请根据文档指引申请进群，私信群主获取解决方案")
        elif len([item for item in map_seed if item == 0]) == 4:
            print("=====> 地图种子信息加载失败")
            print("=====> 请根据文档指引申请进群，私信群主获取解决方案")
        else:
            map_struct_data = FileHelper().read_json_data(map_struct_file)
            self._map_struct_fill_data(map_struct_data, map_seed)
            self._save_local_seed_data(map_struct_data, self._save_file_path)

    def _generate_map_struct_file_path(self, map_hash):
        map_cache_name = "{}.json".format(map_hash)
        return os.path.join(self._static_map_path, map_cache_name)

    def _map_struct_fill_data(self, map_struct_data, map_seed):
        self._shuffle_helper = ShuffleHelper(map_seed)
        if isinstance(map_struct_data, dict):
            self._ensure_map_key_sorted(map_struct_data)
            self._reset_map_card_type(map_struct_data)

    @staticmethod
    def _save_local_seed_data(map_struct_data, seed_data_path):
        if isinstance(map_struct_data, dict) and len(map_struct_data):
            FileHelper().write_json_data(seed_data_path, map_struct_data)
            print("=====> 当前游戏的地图数据生成成功")

    def _ensure_map_key_sorted(self, map_struct_data):
        self._adjust_data_dict(map_struct_data, "blockTypeData")
        self._adjust_data_dict(map_struct_data, "levelData")

    def _reset_map_card_type(self, map_struct_data):
        type_list = self._generate_shuffle_list(map_struct_data)
        card_list = self._generate_card_list(map_struct_data)
        card_list = [item for item in card_list if item["type"] == 0]
        for card_item, card_type in zip(card_list, type_list):
            card_item["type"] = card_type

    @staticmethod
    def _adjust_data_dict(data_dict, sort_key):
        data_dict[sort_key] = dict(sorted(data_dict[sort_key].items(), key=lambda item: int(item[0])))

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

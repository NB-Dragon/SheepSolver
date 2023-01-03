#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import os
from core.data.ShuffleHelper import ShuffleHelper
from hepler.FileHelper import FileHelper


class StaticDataGenerator(object):
    def __init__(self, static_map_path):
        self._static_map_path = static_map_path

    def generate_map_data(self, map_hash, map_seed_dict):
        origin_map_data = self._load_map_cache_data(map_hash)
        if isinstance(origin_map_data, dict):
            self._ensure_map_key_sorted(origin_map_data)
            block_type_data, shuffle_seed = origin_map_data["blockTypeData"], map_seed_dict["map_seed"]
            block_type_list = self._generate_shuffle_list(block_type_data, shuffle_seed)
            self._reset_map_data_type(block_type_list, origin_map_data)
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
        block_type_list = []
        for key, count in block_type_data.items():
            block_type_list.extend([int(key)] * count * 3)
        ShuffleHelper(map_seed).shuffle(block_type_list)
        return block_type_list

    @staticmethod
    def _reset_map_data_type(block_type_list, map_cache_data):
        current_index = 0
        for level, level_data in map_cache_data["levelData"].items():
            for each_card in level_data:
                if each_card["type"] == 0:
                    each_card["type"] = block_type_list[current_index]
                    current_index += 1

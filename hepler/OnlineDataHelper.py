#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import json
import os
import time
import certifi
import urllib3
from hepler.FileHelper import FileHelper
from hepler.MapDataHelper import MapDataHelper


class OnlineDataHelper(object):
    def __init__(self, code_entrance_path):
        self._code_entrance_path = code_entrance_path
        self._static_map_path = os.path.join(self._code_entrance_path, "static", "map")
        self._final_data_path = os.path.join(self._code_entrance_path, "online_data.json")
        self._map_data_helper = MapDataHelper(self._static_map_path)
        self._map_seed_dict = dict()
        self._map_hash = None

    def create_online_data(self, map_summary_content):
        summary_data = json.loads(map_summary_content)
        self._reset_map_hash_and_seed(summary_data)
        self._load_map_struct_data()
        self._generate_final_map_file()

    def _reset_map_hash_and_seed(self, response_data):
        self._map_seed_dict["map_seed"] = response_data["data"]["map_seed"]
        self._map_seed_dict["map_seed_2"] = response_data["data"]["map_seed_2"]
        print("=====> 当前游戏的随机种子已更新")
        self._map_hash = response_data["data"]["map_md5"][1]
        print("=====> 当前游戏的地图结构密钥已更新")

    def _load_map_struct_data(self):
        map_cache_file = self._generate_map_cache_path()
        if not self._map_cache_file_match_date(map_cache_file):
            map_struct_content = self._request_map_struct_data()
            self._save_map_struct_data(map_cache_file, map_struct_content)

    def _generate_final_map_file(self):
        map_real_data = self._map_data_helper.generate_map_data(self._map_hash, self._map_seed_dict)
        if isinstance(map_real_data, dict):
            FileHelper().write_json_data(self._final_data_path, map_real_data)
            print("=====> 当前游戏的地图数据生成成功")
        else:
            print("=====> 当前游戏的地图数据生成失败")

    def _request_map_struct_data(self):
        map_link = self._generate_map_struct_request_link()
        return self._request_get_method(map_link)

    def _save_map_struct_data(self, map_cache_file, map_struct_data):
        if isinstance(map_struct_data, str) and len(map_struct_data):
            FileHelper().write_file_content(map_cache_file, map_struct_data)
            print("=====> 地图初始结构缓存成功: {}".format(self._map_hash))

    def _generate_map_struct_request_link(self):
        return "https://cat-match-static.easygame2021.com/maps/{}.txt".format(self._map_hash)

    @staticmethod
    def _request_get_method(request_link):
        try:
            pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=30)
            response = pool_manager.request("GET", request_link, preload_content=False)
            content = response.read()
            response.close()
            return content.decode()
        except Exception as e:
            print("[GET] 请求异常，异常信息为: {}".format(str(e)))
            return None

    def _generate_map_cache_path(self):
        map_cache_name = "{}.json".format(self._map_hash)
        return os.path.join(self._static_map_path, map_cache_name)

    def _map_cache_file_match_date(self, map_cache_file):
        if os.path.isfile(map_cache_file):
            system_date = self._get_current_date()
            modify_date = self._get_file_modify_date(map_cache_file)
            return system_date == modify_date
        return False

    @staticmethod
    def _get_current_date():
        return time.strftime("%Y-%m-%d", time.localtime())

    @staticmethod
    def _get_file_modify_date(file_path):
        modify_time_second = os.path.getmtime(file_path)
        modify_time = time.localtime(modify_time_second)
        return time.strftime("%Y-%m-%d", modify_time)

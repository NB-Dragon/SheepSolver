#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import os
import time
import certifi
import urllib3
from hepler.FileHelper import FileHelper


class OnlineDataAnalyzer(object):
    def __init__(self, project_helper, static_map_link):
        self._final_data_path = project_helper.get_project_file_path("online_data")
        self._static_map_path = project_helper.get_project_directory_path("static_map")
        self._static_map_link = static_map_link

    def download_map_struct_data(self, summary_data: dict):
        if summary_data["err_code"] == 0:
            map_hash = self._get_game_map_hash(summary_data)
            self._create_local_struct_data(map_hash)

    def _create_local_struct_data(self, map_hash):
        map_cache_file = self._generate_map_cache_path(map_hash)
        if not self._is_file_up_to_date(map_cache_file):
            map_struct_content = self._request_map_struct_data(map_hash)
            self._save_local_struct_data(map_cache_file, map_struct_content, map_hash)

    def _request_map_struct_data(self, map_hash):
        map_struct_link = self._generate_map_struct_request_link(map_hash)
        return self._request_get_method(map_struct_link)

    @staticmethod
    def _save_local_struct_data(map_cache_file, map_struct_data, map_hash):
        if isinstance(map_struct_data, str) and len(map_struct_data):
            FileHelper().write_file_content(map_cache_file, map_struct_data)
            print("=====> 地图初始结构缓存成功: {}".format(map_hash))
        else:
            print("=====> 地图初始结构缓存失败: {}".format(map_hash))

    def _generate_map_struct_request_link(self, map_hash):
        return "{}/{}.txt".format(self._static_map_link, map_hash)

    @staticmethod
    def _request_get_method(request_link):
        try:
            pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=30)
            response = pool_manager.request("GET", request_link, preload_content=False)
            content, status = response.read(), response.status
            response.close()
            return content.decode() if status in [200] else None
        except Exception as e:
            print("[GET] 请求异常，异常信息为: {}".format(str(e)))
            return None

    def _generate_map_cache_path(self, map_hash):
        map_cache_name = "{}.json".format(map_hash)
        return os.path.join(self._static_map_path, map_cache_name)

    def _is_file_up_to_date(self, file_path):
        if os.path.isfile(file_path):
            system_date = self._get_current_date()
            modify_date = self._get_file_modify_date(file_path)
            return system_date == modify_date
        return False

    @staticmethod
    def _get_game_map_hash(summary_data):
        print("=====> 当前游戏的地图结构密钥已更新")
        return summary_data["data"]["map_md5"][1]

    @staticmethod
    def _get_current_date():
        return time.strftime("%Y-%m-%d", time.localtime())

    @staticmethod
    def _get_file_modify_date(file_path):
        modify_time_second = os.path.getmtime(file_path)
        modify_time = time.localtime(modify_time_second)
        return time.strftime("%Y-%m-%d", modify_time)

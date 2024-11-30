#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import os
import time
from core.tool.GameLinkController import GameLinkController
from helper.FileHelper import FileHelper
from helper.RequestHelper import RequestHelper


class OnlineDataAnalyzer(object):
    def __init__(self, project_helper):
        self._project_helper = project_helper
        self._request_helper = RequestHelper()
        self._prepare_runtime_param()

    def _prepare_runtime_param(self):
        link_config = self._project_helper.get_project_config("protect", "link")
        self._game_link_controller = GameLinkController(link_config)
        self._static_map_link = self._game_link_controller.get_static_map_link()
        self._static_map_path = self._project_helper.get_project_path("static_map")

    def create_map_struct_cache(self, map_hash):
        map_struct_link = self._generate_map_struct_request_link(map_hash, "map")
        return self._request_helper.request_get_method(map_struct_link)

    def create_map_struct_file(self, map_hash):
        map_struct_link = self._generate_map_struct_request_link(map_hash, "txt")
        map_struct_file = self._generate_map_struct_file_path(map_hash)
        if self._is_file_up_to_date(map_struct_file):
            print("=====> 地图初始结构加载缓存: {}".format(map_hash))
        else:
            map_struct_data = self._request_helper.request_get_method(map_struct_link)
            self._save_local_struct_data(map_struct_data, map_struct_file, map_hash)

    def _generate_map_struct_request_link(self, map_hash, postfix):
        return "{}/{}.{}".format(self._static_map_link, map_hash, postfix)

    def _generate_map_struct_file_path(self, map_hash):
        map_cache_name = "{}.json".format(map_hash)
        return os.path.join(self._static_map_path, map_cache_name)

    @staticmethod
    def _save_local_struct_data(map_struct_data, map_struct_file, map_hash):
        if isinstance(map_struct_data, bytes) and len(map_struct_data):
            FileHelper().write_bytes_data(map_struct_file, map_struct_data)
            print("=====> 地图初始结构缓存成功: {}".format(map_hash))
        else:
            print("=====> 地图初始结构缓存失败: {}".format(map_hash))

    def _is_file_up_to_date(self, file_path):
        if os.path.isfile(file_path):
            system_date = self._get_current_date()
            modify_date = self._get_file_modify_date(file_path)
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/20 00:00
# Create User: NB-Dragon
import os
import sys
from helper.FileHelper import FileHelper


class ProjectHelper(object):
    def __init__(self):
        self._code_entrance_path = self._get_application_path()
        self._project_path = self._init_project_path()
        self._project_file = self._init_project_file()
        self._project_config = self._init_project_config()

    def _init_project_path(self):
        result_dict = dict()
        result_dict["static_map"] = os.path.join(self._code_entrance_path, "static", "map")
        result_dict["static_skin"] = os.path.join(self._code_entrance_path, "static", "skin")
        result_dict["static_config"] = os.path.join(self._code_entrance_path, "static", "config")
        result_dict["static_client"] = os.path.join(self._code_entrance_path, "static", "client")
        return result_dict

    def _init_project_file(self):
        result_dict = dict()
        result_dict["skin_info"] = os.path.join(self._project_path["static_skin"], "skin_info.json")
        result_dict["block_info"] = os.path.join(self._project_path["static_skin"], "block_info.json")
        result_dict["topic_info"] = os.path.join(self._project_path["static_skin"], "topic_info.json")
        result_dict["dynamic_config"] = os.path.join(self._project_path["static_config"], "dynamic_config.json")
        result_dict["protect_config"] = os.path.join(self._project_path["static_config"], "protect_config.json")
        result_dict["mahjong_config"] = os.path.join(self._project_path["static_config"], "mahjong_config.json")
        result_dict["client_content"] = os.path.join(self._project_path["static_client"], "application.hint")
        result_dict["client_license"] = os.path.join(self._project_path["static_client"], "application.lic")
        result_dict["client_trusted"] = os.path.join(self._project_path["static_client"], "application.sig")
        result_dict["client_certificate"] = os.path.join(self._project_path["static_client"], "application.pem")
        return result_dict

    def _init_project_config(self):
        dynamic_config = FileHelper().read_json_data(self._project_file["dynamic_config"])
        protect_config = FileHelper().read_json_data(self._project_file["protect_config"])
        mahjong_config = FileHelper().read_json_data(self._project_file["mahjong_config"])
        return {"dynamic": dynamic_config, "protect": protect_config, "mahjong": mahjong_config}

    def get_project_config(self, config_name, config_key):
        return self._project_config.get(config_name).get(config_key)

    def get_project_path(self, key):
        return self._project_path.get(key, None)

    def get_project_file(self, key):
        return self._project_file.get(key, None)

    def get_global_online_data(self):
        return os.path.join(self._code_entrance_path, "online_data.json")

    def get_unique_online_data(self, unique_name, game_type):
        file_name = "{}_{}.json".format(unique_name, game_type)
        return os.path.join(self._code_entrance_path, file_name)

    def _get_application_path(self):
        sys_argv = sys.argv
        if self._is_self_running(sys_argv):
            class_save_path = os.path.split(os.path.abspath(sys_argv[0]))[0]
            script_item_list = class_save_path.split(os.path.sep)
        else:
            script_path = self._get_script_path(sys_argv)
            class_save_path = os.path.split(os.path.abspath(script_path))[0]
            script_item_list = class_save_path.split(os.path.sep)
        return os.path.sep.join(script_item_list)

    @staticmethod
    def _is_self_running(sys_argv: list):
        execute_file_path = os.path.abspath(sys_argv[0])
        return "SheepSolver" in execute_file_path

    @staticmethod
    def _get_script_path(sys_argv: list):
        for index in range(len(sys_argv)):
            if sys_argv[index] in ["-s", "--scripts"]:
                return sys_argv[index + 1]
        return None

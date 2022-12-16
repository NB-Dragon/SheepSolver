#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/15 00:00
# Create User: NB-Dragon
import os
from hepler.FileHelper import FileHelper


class InterfaceTool(object):
    def __init__(self, code_entrance_path):
        self._code_entrance_path = code_entrance_path
        self._project_config_path = os.path.join(self._code_entrance_path, "config.json")
        self._project_config = self._read_project_config()

    def _read_project_config(self):
        return FileHelper().read_json_data(self._project_config_path)

    def _get_user_domain(self):
        return self._project_config["domain"]["user"]

    def _get_static_domain(self):
        return self._project_config["domain"]["static"]

    def get_game_start_link_list(self):
        result_list = list()
        result_list.append(self._project_config["game"]["normal"]["start"])
        result_list.append(self._project_config["game"]["topic"]["start"])
        result_list.append(self._project_config["game"]["tag"]["start"])
        return result_list

    def get_normal_start_link(self):
        user_domain = self._get_user_domain()
        game_start_path = self._project_config["game"]["normal"]["start"]
        return "{}/{}".format(user_domain, game_start_path)

    def get_normal_over_link(self):
        user_domain = self._get_user_domain()
        game_over_path = self._project_config["game"]["normal"]["over"]
        return "{}/{}".format(user_domain, game_over_path)

    def get_topic_join_link(self):
        user_domain = self._get_user_domain()
        game_join_path = self._project_config["game"]["topic"]["join"]
        return "{}/{}".format(user_domain, game_join_path)

    def get_topic_start_link(self):
        user_domain = self._get_user_domain()
        game_start_path = self._project_config["game"]["topic"]["start"]
        return "{}/{}".format(user_domain, game_start_path)

    def get_topic_over_link(self):
        user_domain = self._get_user_domain()
        game_over_path = self._project_config["game"]["topic"]["over"]
        return "{}/{}".format(user_domain, game_over_path)

    def get_tag_start_link(self):
        user_domain = self._get_user_domain()
        game_start_path = self._project_config["game"]["tag"]["start"]
        return "{}/{}".format(user_domain, game_start_path)

    def get_tag_over_link(self):
        user_domain = self._get_user_domain()
        game_over_path = self._project_config["game"]["tag"]["over"]
        return "{}/{}".format(user_domain, game_over_path)

    def get_static_map_link(self):
        static_domain = self._get_static_domain()
        map_path = self._project_config["other"]["static_map"]
        return "{}/{}".format(static_domain, map_path)

    def get_topic_info_link(self):
        user_domain = self._get_user_domain()
        topic_info_path = self._project_config["other"]["topic_info"]
        return "{}/{}".format(user_domain, topic_info_path)

    def get_skin_info_link(self):
        user_domain = self._get_user_domain()
        skin_info_path = self._project_config["other"]["skin_info"]
        return "{}/{}".format(user_domain, skin_info_path)

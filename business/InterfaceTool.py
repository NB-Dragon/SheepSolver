#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/15 00:00
# Create User: NB-Dragon


class InterfaceTool(object):
    def __init__(self, project_helper):
        self._project_config = project_helper.get_project_config()
        self._link_config = self._project_config["link"]

    def _get_user_domain(self):
        return self._link_config["domain"]["user"]

    def _get_static_domain(self):
        return self._link_config["domain"]["static"]

    def get_game_start_list(self):
        return [item["start"] for item in self._link_config["game"].values()]

    def get_normal_start_link(self):
        user_domain = self._get_user_domain()
        game_start_path = self._link_config["game"]["normal"]["start"]
        return "{}/{}".format(user_domain, game_start_path)

    def get_normal_over_link(self):
        user_domain = self._get_user_domain()
        game_over_path = self._link_config["game"]["normal"]["over"]
        return "{}/{}".format(user_domain, game_over_path)

    def get_topic_join_link(self):
        user_domain = self._get_user_domain()
        game_join_path = self._link_config["game"]["topic"]["join"]
        return "{}/{}".format(user_domain, game_join_path)

    def get_topic_start_link(self):
        user_domain = self._get_user_domain()
        game_start_path = self._link_config["game"]["topic"]["start"]
        return "{}/{}".format(user_domain, game_start_path)

    def get_topic_over_link(self):
        user_domain = self._get_user_domain()
        game_over_path = self._link_config["game"]["topic"]["over"]
        return "{}/{}".format(user_domain, game_over_path)

    def get_tag_start_link(self):
        user_domain = self._get_user_domain()
        game_start_path = self._link_config["game"]["tag"]["start"]
        return "{}/{}".format(user_domain, game_start_path)

    def get_tag_over_link(self):
        user_domain = self._get_user_domain()
        game_over_path = self._link_config["game"]["tag"]["over"]
        return "{}/{}".format(user_domain, game_over_path)

    def get_static_map_link(self):
        static_domain = self._get_static_domain()
        map_path = self._link_config["other"]["static_map"]
        return "{}/{}".format(static_domain, map_path)

    def get_topic_info_link(self):
        user_domain = self._get_user_domain()
        topic_info_path = self._link_config["other"]["topic_info"]
        return "{}/{}".format(user_domain, topic_info_path)

    def get_skin_info_link(self):
        user_domain = self._get_user_domain()
        skin_info_path = self._link_config["other"]["skin_info"]
        return "{}/{}".format(user_domain, skin_info_path)

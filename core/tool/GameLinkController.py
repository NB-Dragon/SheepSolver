#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/12/15 00:00
# Create User: NB-Dragon
import urllib.parse


class GameLinkController(object):
    def __init__(self, link_config):
        self._link_config = link_config

    def get_user_domain_link(self):
        return self._link_config["domain"]["user"]

    def get_static_domain_link(self):
        return self._link_config["domain"]["static"]

    def get_game_start_list(self):
        return [item["start"] for item in self._link_config["game"].values()]

    def get_game_config(self, game_type):
        return self._link_config["game"][game_type]

    def get_static_map_link(self):
        static_domain = self.get_static_domain_link()
        map_path = self._link_config["other"]["static_map"]
        return urllib.parse.urljoin(static_domain, map_path)

    def get_personal_info_link(self):
        user_domain = self.get_user_domain_link()
        personal_info_path = self._link_config["other"]["personal_info"]
        return urllib.parse.urljoin(user_domain, personal_info_path)

    def get_topic_info_link(self):
        user_domain = self.get_user_domain_link()
        topic_info_path = self._link_config["other"]["topic_info"]
        return urllib.parse.urljoin(user_domain, topic_info_path)

    def get_skin_info_link(self):
        user_domain = self.get_user_domain_link()
        skin_info_path = self._link_config["other"]["skin_info"]
        return urllib.parse.urljoin(user_domain, skin_info_path)

    def get_challenge_info_link(self):
        user_domain = self.get_user_domain_link()
        challenge_info_path = self._link_config["other"]["challenge_info"]
        return urllib.parse.urljoin(user_domain, challenge_info_path)

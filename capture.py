#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import json
import urllib.parse
from core.map.OnlineDataAnalyzer import OnlineDataAnalyzer
from core.map.StaticDataGenerator import StaticDataGenerator
from core.tool.GameLinkController import GameLinkController
from helper.ProjectHelper import ProjectHelper


class DataAnalyzer(object):
    def __init__(self):
        self._project_helper = ProjectHelper()
        self._game_link_controller = self._generate_game_link_controller()
        self._game_start_list = self._game_link_controller.get_game_start_list()
        self._online_data_analyzer = OnlineDataAnalyzer(self._project_helper)
        self._static_data_generator = StaticDataGenerator(self._project_helper)

    def response(self, flow):
        link_parse_result = urllib.parse.urlparse(flow.request.url)
        if link_parse_result.netloc == "cat-match.easygame2021.com":
            if self._is_game_start_link(link_parse_result.path):
                response_data = json.loads(flow.response.content)
                self._handle_response_result(response_data)
        elif link_parse_result.netloc == "cat-match-static.easygame2021.com":
            if self._is_game_resource_data(flow.response.content):
                print(flow.response.content.decode())

    def _generate_game_link_controller(self):
        link_config = self._project_helper.get_project_config("normal", "link")
        return GameLinkController(link_config)

    def _is_game_start_link(self, request_path):
        match_list = [item for item in self._game_start_list if request_path.endswith(item)]
        return len(match_list) != 0

    @staticmethod
    def _is_game_resource_data(bytes_data):
        resource_name_list = [b"gd_language", b"gd_skin_list", b"gd_game_topic_list", b"gd_block_topic_slot_data"]
        match_list = [item for item in resource_name_list if item in bytes_data]
        return len(match_list) != 0

    def _handle_response_result(self, response_data):
        map_hash = response_data["data"]["map_md5"][1]
        map_seed = response_data["data"]["map_seed"]
        self._online_data_analyzer.create_map_struct_file(map_hash)
        self._static_data_generator.fill_seed_data_into_file(map_hash, map_seed)


addons = [DataAnalyzer()]

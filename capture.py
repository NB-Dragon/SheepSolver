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
        self._static_map_link = self._game_link_controller.get_static_map_link()
        self._game_start_list = self._game_link_controller.get_game_start_list()
        self._static_map_path = self._project_helper.get_project_directory_path("static_map")
        self._online_data_analyzer = OnlineDataAnalyzer(self._static_map_path, self._static_map_link)
        self._static_data_generator = StaticDataGenerator(self._static_map_path)

    def response(self, flow):
        link_parse_result = urllib.parse.urlparse(flow.request.url)
        if link_parse_result.netloc == "cat-match.easygame2021.com":
            request_header = dict(flow.request.headers)
            if self._is_game_start_link(link_parse_result.path):
                response_data = json.loads(flow.response.content)
                self._handle_response_result(response_data, request_header)
        elif link_parse_result.netloc == "cat-match-static.easygame2021.com":
            if self._is_game_resource_data(flow.response.content):
                print(flow.response.content.decode())

    def _generate_game_link_controller(self):
        link_config = self._project_helper.get_project_config()["link"]
        return GameLinkController(link_config)

    def _is_game_start_link(self, request_path):
        match_list = [item for item in self._game_start_list if item in request_path]
        return len(match_list) != 0

    @staticmethod
    def _is_game_resource_data(bytes_data):
        resource_name_list = [b"gd_language", b"gd_skin_list", b"gd_game_topic_list", b"gd_block_topic_slot_data"]
        match_list = [item for item in resource_name_list if item in bytes_data]
        return len(match_list) != 0

    def _handle_response_result(self, response_data, header=None):
        header = {key.lower(): value for key, value in header.items()}
        print("=====> 当前用户token为: {}".format(header.get("t")))
        save_file_path = self._project_helper.get_project_file_path("online_data")
        self._online_data_analyzer.download_map_struct_data(response_data)
        self._static_data_generator.generate_final_map_file(response_data, save_file_path)


addons = [DataAnalyzer()]

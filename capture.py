#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import json
import urllib.parse
from business.InterfaceTool import InterfaceTool
from core.map.OnlineDataAnalyzer import OnlineDataAnalyzer
from core.map.StaticDataGenerator import StaticDataGenerator
from helper.ProjectHelper import ProjectHelper


class DataAnalyzer(object):
    def __init__(self):
        self._project_helper = ProjectHelper()
        self._interface_tool = self._generate_interface_tool()
        self._static_map_link = self._interface_tool.get_static_map_link()
        self._game_start_list = self._interface_tool.get_game_start_list()
        self._static_map_path = self._project_helper.get_project_directory_path("static_map")
        self._online_data_analyzer = OnlineDataAnalyzer(self._static_map_path, self._static_map_link)
        self._static_data_generator = StaticDataGenerator(self._static_map_path)

    def response(self, flow):
        link_parse_result = urllib.parse.urlparse(flow.request.url)
        if link_parse_result.netloc == "cat-match.easygame2021.com":
            request_header = dict(flow.request.headers)
            if self._judge_game_start(link_parse_result.path):
                response_data = json.loads(flow.response.content)
                self._handle_response_result(response_data, request_header)
        elif link_parse_result.netloc == "cat-match-static.easygame2021.com":
            if self._judge_name_important(flow.response.content):
                print(flow.response.content.decode())

    def _generate_interface_tool(self):
        link_config = self._project_helper.get_project_config()["link"]
        return InterfaceTool(link_config)

    @staticmethod
    def _judge_name_important(byte_data):
        important_name_list = [b"gd_game_topic_list", b"gd_skin_list", b"gd_language", b"gd_event_data"]
        for name_item in important_name_list:
            if name_item in byte_data:
                return True
        return False

    def _judge_game_start(self, request_path):
        for item in self._game_start_list:
            if item in request_path:
                return True
        return False

    def _handle_response_result(self, response_data, header=None):
        header = {key.lower(): value for key, value in header.items()}
        print("=====> 当前用户token为: {}".format(header.get("t")))
        save_file_path = self._project_helper.get_project_file_path("online_data")
        self._online_data_analyzer.download_map_struct_data(response_data)
        self._static_data_generator.generate_final_map_file(response_data, save_file_path)


addons = [DataAnalyzer()]

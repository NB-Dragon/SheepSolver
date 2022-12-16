#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import os
import sys
import urllib.parse
from business.InterfaceTool import InterfaceTool
from hepler.OnlineDataHelper import OnlineDataHelper


class DataAnalyzer(object):
    def __init__(self):
        self._code_entrance_path = self._get_project_path()
        self._online_data_helper = OnlineDataHelper(self._code_entrance_path)
        self._interface_tool = InterfaceTool(self._code_entrance_path)
        self._game_start_link_list = self._interface_tool.get_game_start_link_list()

    def response(self, flow):
        link_parse_result = urllib.parse.urlparse(flow.request.url)
        if link_parse_result.netloc == "cat-match.easygame2021.com":
            request_header = dict(flow.request.headers)
            if self._judge_game_start(link_parse_result.path):
                self._handle_response_result(flow.response.content, request_header)

    def _judge_game_start(self, request_path):
        for item in self._game_start_link_list:
            if item in request_path:
                return True
        return False

    def _get_project_path(self):
        sys_argv = sys.argv
        if len(sys_argv) == 1:
            class_save_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
            script_item_list = class_save_path.split(os.path.sep)
        else:
            script_path = self._get_script_path(sys_argv)
            class_save_path = os.path.split(os.path.abspath(script_path))[0]
            script_item_list = class_save_path.split(os.path.sep)
        self._remove_path_item(script_item_list)
        return os.path.sep.join(script_item_list)

    @staticmethod
    def _get_script_path(sys_argv: list):
        for index in range(len(sys_argv)):
            if sys_argv[index] in ["-s", "--script"]:
                return sys_argv[index + 1]
        return None

    @staticmethod
    def _remove_path_item(origin_list):
        relative_path_list = []
        for remove_item in relative_path_list:
            if remove_item in origin_list:
                origin_list.remove(remove_item)

    def _handle_response_result(self, content, header=None):
        header = {key.lower(): value for key, value in header.items()}
        print("=====> 当前用户token为: {}".format(header.get("t")))
        self._online_data_helper.create_online_data(content)


addons = [DataAnalyzer()]

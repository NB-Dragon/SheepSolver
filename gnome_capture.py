#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import base64
import json
import os
import sys
import urllib.parse


class FileHelper(object):
    def read_json_data(self, file_path):
        bytes_data = self.read_bytes_data(file_path) or b"null"
        file_string = bytes_data.decode("utf-8", "surrogatepass")
        return json.loads(file_string)

    @staticmethod
    def read_bytes_data(file_path):
        try:
            reader = open(file_path, "rb")
            content = reader.read()
            reader.close()
            return content
        except Exception as e:
            return None


class ProjectHelper(object):
    def __init__(self):
        self._code_entrance_path = self._get_application_path()
        self._project_path = self._init_project_path()
        self._project_file = self._init_project_file()
        self._project_config = self._init_project_config()

    def _init_project_path(self):
        result_dict = dict()
        result_dict["static_config"] = os.path.join(self._code_entrance_path, "static", "config")
        return result_dict

    def _init_project_file(self):
        result_dict = dict()
        result_dict["protect_config"] = os.path.join(self._project_path["static_config"], "protect_config.json")
        return result_dict

    def _init_project_config(self):
        protect_config = FileHelper().read_json_data(self._project_file["protect_config"])
        return {"protect": protect_config}

    def get_project_config(self, config_name, config_key):
        return self._project_config.get(config_name).get(config_key)

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


class GameLinkController(object):
    def __init__(self, link_config):
        self._link_config = link_config

    def get_game_start_list(self):
        return [item["start"] for item in self._link_config["game"].values()]

    def get_game_seed_list(self):
        return [item["seed"] for item in self._link_config["game"].values()]


class DataAnalyzer(object):
    def __init__(self):
        self._project_helper = ProjectHelper()
        self._prepare_runtime_param()

    def _prepare_runtime_param(self):
        link_config = self._project_helper.get_project_config("protect", "link")
        self._game_link_controller = GameLinkController(link_config)
        self._game_start_list = self._game_link_controller.get_game_start_list()
        self._game_seed_list = self._game_link_controller.get_game_seed_list()

    def response(self, flow):
        link_parse_result = urllib.parse.urlparse(flow.request.url)
        if link_parse_result.netloc == "cat-match.easygame2021.com":
            if self._is_game_start_link(link_parse_result.path):
                self._handle_response_result("game_start", flow.response.content)
            elif self._is_game_seed_link(link_parse_result.path):
                self._handle_response_result("game_seed", flow.response.content)

    def _is_game_start_link(self, request_path):
        match_list = [item for item in self._game_start_list if request_path.endswith(item)]
        return len(match_list) != 0

    def _is_game_seed_link(self, request_path):
        match_list = [item for item in self._game_seed_list if request_path.endswith(item)]
        return len(match_list) != 0

    @staticmethod
    def _handle_response_result(data_type, bytes_data):
        encode_data = base64.b64encode(bytes_data).decode()
        result_dict = {"message_type": data_type, "message_data": encode_data}
        encode_content = json.dumps(result_dict, ensure_ascii=False)
        print("[SheepSolver] {}".format(encode_content), flush=True)


addons = [DataAnalyzer()]

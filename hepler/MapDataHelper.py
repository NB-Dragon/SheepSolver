import json
import os
import time
import certifi
import urllib3
from hepler.FileHelper import FileHelper
from hepler.ShuffleHelper import ShuffleHelper


class MapDataHelper(object):
    def __init__(self, code_entrance_path):
        self._code_entrance_path = code_entrance_path
        self._static_map_path = os.path.join(self._code_entrance_path, "static", "map")
        self._final_data_path = os.path.join(self._code_entrance_path, "online_data.json")
        self._map_seed_dict = dict()

    def update_map_data(self, content):
        response_data = json.loads(content)
        self._map_seed_dict["map_seed"] = response_data["data"]["map_seed"]
        self._map_seed_dict["map_seed_2"] = response_data["data"]["map_seed_2"]
        print("=====> 当前游戏的随机种子已更新")
        map_hash = response_data["data"]["map_md5"][1]
        map_cache_data = self._load_map_cache_data(map_hash)
        self._generate_final_map_data(map_cache_data)

    def _load_map_cache_data(self, map_hash):
        map_cache_file = self._generate_map_cache_path(map_hash)
        if not self._map_cache_file_match_date(map_cache_file):
            map_content = self._request_map_struct_data(map_hash)
            if isinstance(map_content, str) and len(map_content):
                FileHelper().write_file_content(map_cache_file, map_content)
                print("=====> 地图初始结构缓存成功: {}".format(map_hash))
        return FileHelper().read_json_data(map_cache_file)

    def _generate_final_map_data(self, map_cache_data):
        if isinstance(map_cache_data, dict):
            self._ensure_map_key_sorted(map_cache_data)
            block_type_list = self._generate_shuffle_list(map_cache_data["blockTypeData"])
            self._reset_map_data_type(block_type_list, map_cache_data)
            map_cache_data.update(self._map_seed_dict)
            FileHelper().write_json_data(self._final_data_path, map_cache_data)
            print("=====> 当前游戏的地图数据已初始化完毕")

    @staticmethod
    def _request_map_struct_data(map_hash):
        map_link = "https://cat-match-static.easygame2021.com/maps/{}.txt".format(map_hash)
        request_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=30)
        try:
            response = request_manager.request("GET", map_link, preload_content=False)
            content = response.read()
            response.close()
            return content.decode()
        except Exception as e:
            print(str(e))
            return None

    def _generate_shuffle_list(self, block_type_data):
        block_type_list = []
        for key, count in block_type_data.items():
            block_type_list.extend([int(key)] * count * 3)
        ShuffleHelper(self._map_seed_dict["map_seed"]).shuffle(block_type_list)
        return block_type_list

    @staticmethod
    def _reset_map_data_type(block_type_list, map_cache_data):
        current_index = 0
        for level, level_data in map_cache_data["levelData"].items():
            for each_card in level_data:
                if each_card["type"] == 0:
                    each_card["type"] = block_type_list[current_index]
                    current_index += 1

    def _generate_map_cache_path(self, map_hash):
        map_cache_name = "{}.json".format(map_hash)
        return os.path.join(self._static_map_path, map_cache_name)

    def _map_cache_file_match_date(self, map_cache_file):
        if os.path.isfile(map_cache_file):
            system_date = self._get_current_date()
            modify_date = self._get_file_modify_date(map_cache_file)
            return system_date == modify_date
        return False

    @staticmethod
    def _ensure_map_key_sorted(map_cache_data):
        block_type_data = map_cache_data["blockTypeData"]
        map_cache_data["blockTypeData"] = dict(sorted(block_type_data.items(), key=lambda item: int(item[0])))
        level_data = map_cache_data["levelData"]
        map_cache_data["levelData"] = dict(sorted(level_data.items(), key=lambda item: int(item[0])))

    @staticmethod
    def _get_current_date():
        return time.strftime("%Y-%m-%d", time.localtime())

    @staticmethod
    def _get_file_modify_date(file_path):
        modify_time_second = os.path.getmtime(file_path)
        modify_time = time.localtime(modify_time_second)
        return time.strftime("%Y-%m-%d", modify_time)

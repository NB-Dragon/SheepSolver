from mitmproxy import ctx
from datetime import date
import execjs
import json
import os


class Sheep():

    def __init__(self):
        self.seed = [0, 0, 0, 0]
        self.js_code = open("shuffle.js", encoding="utf-8").read()
        self.map_data_path = "./map_data.txt"
        self.map_data_topic_path = "./map_data_topic.txt"

    def response(self, flow):
        """ 接口响应方法 """
        if "map_info_ex" in flow.request.path:
            # 获取随机种子的接口，随机种子存储到self.seed中
            response = json.loads(flow.response.content)
            self.seed = response["data"]["map_seed"]
            self.make_map_data(False)
        elif "topic/game_start" in flow.request.path:
            # 今日话题获取随机种子的接口
            response = json.loads(flow.response.content)
            self.seed = response["data"]["map_seed"]
            self.make_map_data(True)
        elif "/maps/" in flow.request.path:
            # 获取地图数据的接口，不解析第一关
            if "046ef1bab26e5b9bfe2473ded237b572" in flow.request.path:
                # 游戏第一关
                return
            if "a92ee0f5f116b13b7b594e67a53defad" in flow.request.path:
                # 今日话题第一关
                return
            # 解析原始地图数据
            response = json.loads(flow.response.content)
            # 判断是否是话题挑战
            is_topic = False
            if response["levelKey"] == 100000 + date.today().day:
                is_topic = True
            # 保存原始地图数据
            map_data_path = self.get_map_data_path(is_topic)
            with open(map_data_path, "w") as f:
                f.write(json.dumps(response, indent=4))
                f.close()
            self.make_map_data(is_topic)

    def get_map_data_path(self, is_topic):
        """ 获取文件路径 """
        if is_topic:
            return self.map_data_topic_path
        else:
            return self.map_data_path
    
    def write_outside_solve_data(self, origin_data):
        save_path = "/home/am/文档/PycharmProjects/SheepSlover"
        slove_map_data = {}
        for level, data_list in origin_data["levelData"].items():
            slove_map_data[level] = []
            for data_item in data_list:
                slove_item = {"id": data_item["id"],
                "type": data_item["type"],
                "rolNum": data_item["rolNum"],
                "rowNum": data_item["rowNum"]}
                slove_map_data[level].append(slove_item)
        writer = open(save_path, "w")
        writer.write(json.dumps(slove_map_data))
        writer.close()
        

    def make_map_data(self, is_topic):
        """ 制作地图数据 """

        print("==========================================")

        # 判断原始地图文件是否存在
        map_data_path = self.get_map_data_path(is_topic)
        if not os.path.isfile(map_data_path):
            return

        # 读取原始地图数据
        map_data = json.loads(open(map_data_path).read())

        # 根据"blockTypeData"字段按顺序生成所有类型的方块，存放到数组
        block_type_data = map_data["blockTypeData"]
        block_types = []
        for i in range(1, 16+1):
            block_type = str(i)
            if block_type in block_type_data:
                count = block_type_data[block_type] * 3
                block_types.extend([i] * count)

        # 调用js方法将数组打乱，打乱后的结果和游戏的一样
        block_types = execjs.compile(self.js_code).call(
            "shuffle", block_types, self.seed)
        print(block_types)

        # 将游戏的层数排序
        level_data = map_data["levelData"]
        layers = list(level_data.keys())
        layers.sort(key=lambda x: int(x))

        # 为了方便three.js按顺序读取层数，所以将层数保存起来
        map_data["layers"] = layers

        # 将打乱后的图案按顺序填充到每个方块的"type"字段里
        index = 0
        for layer in layers:
            for block_data in level_data[layer]:
                if block_data["type"] > 0:
                    continue
                block_data["type"] = block_types[index]
                index += 1

        # 保存地图数据
        data_string = f"const map_data = {json.dumps(map_data, indent=4)};"
        save_path = "./html/map_data.js"
        with open(save_path, "w") as f:
            f.write(data_string)
            f.close()

        print("==========================================")


addons = [Sheep()]

from mitmproxy import ctx
import datetime
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
            # 解析原始地图数据
            response = json.loads(flow.response.content)
            # 不解析第一关
            if response["levelKey"] < 90000:
                return
            # 判断是否是话题挑战
            is_topic = (response["levelKey"] >= 100000)
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

    @staticmethod
    def write_outside_solve_data(origin_data):
        save_path = "path/to/your/SheepSolver/online_data.json"
        writer = open(save_path, "w")
        writer.write(json.dumps(origin_data["levelData"]))
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

        # 判断是否使用了旧地图数据
        # !!!: 当前只判断了day，在不同月份使用相同day的地图文件不会出现提示
        day = int(map_data["levelKey"]) % 100
        if day != datetime.datetime.today().day:
            ctx.log.error(f"当前使用的地图数据文件为{day}号地图，请删除游戏缓存后重新进入游戏！")

        # 根据"blockTypeData"字段按顺序生成所有类型的方块，存放到数组
        block_type_data = map_data["blockTypeData"]
        block_types = []
        for i in range(1, 16 + 1):
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
        map_data["operations"] = []
        data_string = f"const map_data = {json.dumps(map_data, indent=4)};"
        save_path = "./html/map_data.js"
        with open(save_path, "w") as f:
            f.write(data_string)
            f.close()

        print("==========================================")
        self.write_outside_solve_data(map_data)
        print("==========================================")


addons = [Sheep()]

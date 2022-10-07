from mitmproxy import ctx
import execjs
import json
import os


class Sheep():

    def __init__(self):
        self.seed = [0, 0, 0, 0]
        self.js_code = open("shuffle.js", encoding="utf-8").read()
        self.map_data_path = "./map_data.txt"
        self.solve_origin_path = "path/to/your/SheepSolver/online_data.json"

    def response(self, flow):
        """ 接口响应方法 """
        if "map_info_ex" in flow.request.path:
            # 获取随机种子的接口，随机种子存储到self.seed中
            response = json.loads(flow.response.content)
            self.seed = response["data"]["map_seed"]
            self.make_map_data()
        elif "maps" in flow.request.path:
            # 获取地图数据的接口，不解析第一关
            if "046ef1bab26e5b9bfe2473ded237b572" in flow.request.path:
                return
            # 保存地图数据
            response = json.loads(flow.response.content)
            with open(self.map_data_path, "w") as f:
                f.write(json.dumps(response, indent=4))
                f.close()
            self.make_map_data()

    def make_map_data(self):
        """ 制作地图数据 """

        print("==========================================")

        # 判断地图文件是否存在
        if not os.path.exists(self.map_data_path):
            return

        # 读取原始地图数据
        map_data = json.loads(open(self.map_data_path).read())

        # 根据"blockTypeData"字段按顺序生成所有类型的方块，存放到数组
        block_type_data = map_data["blockTypeData"]
        block_types = []
        for i in range(1, 16+1):
            block_type = str(i)
            if block_type in block_type_data:
                count = block_type_data[block_type] * 3
                block_types.extend([i] * count)

        # 调用js方法将数组打乱，打乱后的结果和游戏的一样
        block_types = execjs.compile(self.js_code).call("shuffle", block_types, self.seed)
        print(block_types)

        # 将游戏的层数排序
        level_data = map_data["levelData"]
        layers = list(level_data.keys())
        layers.sort(key=lambda x:int(x))

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
        save_path = "./three.js/examples/map_data.js"
        with open(save_path, "w") as f:
            f.write(data_string)
            f.close()

        print("==========================================")

        slove_map_data = {}
        for level, data_list in map_data["levelData"].items():
            slove_map_data[level] = []
            for data_item in data_list:
                slove_item = {"type": data_item["type"],
                "min_x": data_item["rolNum"],
                "min_y": data_item["rowNum"],
                "max_x": data_item["rolNum"] + 8,
                "max_y": data_item["rowNum"] + 8}
                slove_map_data[level].append(slove_item)
        writer = open(self.solve_origin_path, "w")
        writer.write(json.dumps(slove_map_data))
        writer.close()


addons = [Sheep()]
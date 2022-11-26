import time
from business.SheepSolver import SheepSolver
from hepler.FileHelper import FileHelper


def read_online_data():
    online_file_path = "online_data.json"
    return FileHelper().read_json_data(online_file_path)

#normal: 默认模式，该模式下取牌顺序由程序进度决定
#reverse: 反转模式，该模式下取牌顺序由卡牌的逆序号决定，序号大的优先
#random: 随机模式，该模式下取牌顺序完全随机
#top-first: 高层优先模式，该模式下取牌顺序由卡牌的层数决定，高层优先
mode=sys.argv[1]
if mode == "1":
	mode="normal"
elif mode == "2":
	mode="reverse"
elif mode == "3":
	mode="random"
elif mode == "4":
	mode="top-first"
else:
	mode="normal"

if __name__ == '__main__':
    sheep_solver = SheepSolver("normal", 0.8, True)
    sheep_solver.init_card_data(read_online_data())
    start_time = time.time()
    sheep_solver.solve()
    end_time = time.time()
    print(sheep_solver.generate_card_id_result())
    print("计算用时: {}".format(end_time - start_time))

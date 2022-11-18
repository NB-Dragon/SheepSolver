import time
from business.SheepSolver import SheepSolver
from hepler.FileHelper import FileHelper


def read_online_data():
    online_file_path = "online_data.json"
    return FileHelper().read_json_data(online_file_path)


if __name__ == '__main__':
    sheep_solver = SheepSolver("normal", 0.8, True)
    sheep_solver.init_card_data(read_online_data())
    start_time = time.time()
    sheep_solver.solve()
    end_time = time.time()
    print(sheep_solver.generate_card_id_result())
    print("计算用时: {}".format(end_time - start_time))

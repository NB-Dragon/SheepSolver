#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import json
import time
from business.SheepSolver import SheepSolver
from helper.FileHelper import FileHelper
from helper.InputHelper import InputHelper
from helper.ProjectHelper import ProjectHelper


def read_global_config():
    return ProjectHelper().get_project_config("normal", "global")


def read_solve_algorithm():
    input_parser = InputHelper()
    runtime_arguments = input_parser.get_runtime_arguments()
    return runtime_arguments.mode


def read_online_data():
    online_file_path = "online_data.json"
    return FileHelper().read_json_data(online_file_path)


if __name__ == '__main__':
    global_config, algorithm = read_global_config(), read_solve_algorithm()
    sheep_solver = SheepSolver(global_config, algorithm)
    sheep_solver.load_map_data(read_online_data())
    start_time = time.time()
    sheep_solver.solve()
    end_time = time.time()
    print(json.dumps(sheep_solver.generate_card_id_result()))
    print("计算用时: {}".format(end_time - start_time))

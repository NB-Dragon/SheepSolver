#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import time
from core.tool.GamePoolController import GamePoolController
from helper.ProjectHelper import ProjectHelper


class SheepSolver(object):
    def __init__(self, solve_type):
        self._global_config = self._generate_global_config()
        self._game_pool_controller = GamePoolController(solve_type, self._global_config)

        self._start_time = None
        self._iteration_time = 0
        self._current_progress = 0
        self._maximum_progress = 0
        self._card_count = 0
        self._pick_list = []
        self._situation_history = set()

    def load_map_data(self, map_data: dict):
        self._game_pool_controller.init_map_data(map_data)
        self._game_pool_controller.prepare_game_data()
        self._card_count = self._game_pool_controller.get_all_card_count()

    def solve(self):
        self._show_solving_progress()
        self._record_current_progress()
        head_list = self._game_pool_controller.generate_head_list()
        head_list = self._game_pool_controller.ensure_head_list_alive(head_list)
        head_list = self._game_pool_controller.ensure_head_list_disappear(head_list, self._current_progress)
        for head_item in head_list:
            self._generate_current_iteration_time()
            if self._check_programme_can_continue() is False:
                break
            self._operation_pick_card(head_item)
            head_fingerprint = self._game_pool_controller.generate_head_fingerprint()
            if head_fingerprint in self._situation_history:
                self._operation_recover_card(head_item)
                continue
            else:
                self._situation_history.add(head_fingerprint)
            self.solve()
            if not self._game_pool_controller.is_game_over():
                self._operation_recover_card(head_item)
            else:
                break

    @staticmethod
    def _generate_global_config():
        return ProjectHelper().get_project_config("normal", "global")

    def _generate_current_iteration_time(self):
        if isinstance(self._start_time, float):
            self._iteration_time = time.time() - self._start_time
        else:
            self._start_time = time.time()
            self._iteration_time = 0

    def _check_programme_can_continue(self):
        if self._is_solver_in_time_limit():
            return self._is_solver_progress_meets_expect()
        else:
            return False

    def _is_solver_in_time_limit(self):
        time_limit = self._global_config["time_limit"]
        return True if time_limit < 0 else self._iteration_time <= time_limit

    def _is_solver_progress_meets_expect(self):
        expect_progress = self._global_config["expect_progress"]
        expect_time, expect_progress = expect_progress["time"], expect_progress["percentage"]
        detect_result = self._iteration_time <= expect_time or self._maximum_progress >= expect_progress
        return True if expect_time < 0 else detect_result

    def _show_solving_progress(self):
        if self._global_config["show_progress"]:
            print("当前进度为: {}/{}".format(len(self._pick_list), self._card_count))

    def _record_current_progress(self):
        card_list = [item for item in self._pick_list if item >= 0]
        self._current_progress = len(card_list) / self._card_count
        if self._current_progress > self._maximum_progress:
            self._maximum_progress = self._current_progress

    def _operation_pick_card(self, card_index):
        self._game_pool_controller.pick_card(card_index)
        self._pick_list.append(card_index)

    def _operation_recover_card(self, card_index):
        self._game_pool_controller.recover_card(card_index)
        self._pick_list.remove(card_index)

    def _generate_card_detail_dict(self):
        return self._game_pool_controller.get_all_card_dict()

    @staticmethod
    def _get_card_id_from_detail(card_detail_dict, index):
        if index in card_detail_dict:
            return card_detail_dict[index].get_card_id()
        else:
            return "0-0-0"

    @staticmethod
    def _get_card_type_from_detail(card_detail_dict, index):
        if index in card_detail_dict:
            return card_detail_dict[index].get_card_type()
        else:
            return index

    def _generate_card_id_list(self, card_detail_dict, card_list):
        result_list = list()
        for card_item in card_list:
            result_item = self._get_card_id_from_detail(card_detail_dict, card_item)
            result_list.append(result_item)
        return result_list

    def _generate_card_type_list(self, card_detail_dict, card_list):
        result_list = list()
        for card_item in card_list:
            card_type = self._get_card_type_from_detail(card_detail_dict, card_item)
            result_list.append({"index": card_item, "type": card_type})
        return result_list

    def generate_card_index_result(self):
        if self._game_pool_controller.is_game_over():
            return list(self._pick_list)
        else:
            return None

    def generate_card_id_result(self):
        if self._game_pool_controller.is_game_over():
            card_detail_dict = self._generate_card_detail_dict()
            return self._generate_card_id_list(card_detail_dict, self._pick_list)
        else:
            return None

    def generate_card_type_result(self):
        if self._game_pool_controller.is_game_over():
            card_detail_dict = self._generate_card_detail_dict()
            return self._generate_card_type_list(card_detail_dict, self._pick_list)
        else:
            return None

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import time
from core.card.CardContainer import CardContainer
from core.pool.OperationPool import OperationPool
from core.pool.ResidualPool import ResidualPool
from hepler.ProjectHelper import ProjectHelper


class SheepSolver(object):
    def __init__(self, sort_mode):
        self._global_config = self._generate_global_config()
        self._show_progress_method = self._generate_show_progress_method()

        self._card_container = CardContainer()
        self._operation_pool = OperationPool(self._card_container, sort_mode)
        self._residual_pool = ResidualPool(self._card_container)

        self._start_time = None
        self._iteration_time = 0
        self._current_progress = 0
        self._maximum_progress = 0
        self._card_count = 0
        self._pick_list = []
        self._situation_history = set()

    def init_card_data(self, map_data: dict):
        map_level_data = dict(sorted(map_data["levelData"].items(), key=lambda item: int(item[0])))
        for level, level_data in map_level_data.items():
            self._card_count += len(level_data)
            self._card_container.append_level_card(level_data)
        self._operation_pool.generate_head_list()

    def solve(self):
        self._show_progress_method()
        self._record_current_progress()
        head_list = self._operation_pool.get_head_key_list()
        head_list = self._get_head_list_for_alive(head_list)
        head_list = self._get_head_list_sorted_by_residual(head_list)
        for head_item in head_list:
            self._generate_current_iteration_time()
            if self._check_programme_can_continue() is False:
                break
            self._operation_pick_card(head_item)
            head_fingerprint = self._operation_pool.generate_head_description()
            if head_fingerprint in self._situation_history:
                self._operation_recover_card(head_item)
                continue
            else:
                self._situation_history.add(head_fingerprint)
            self.solve()
            if not self._operation_pool.is_game_over():
                self._operation_recover_card(head_item)
            else:
                break

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

    def _is_solver_progress_meets_expect(self):
        expect_progress = self._global_config["expect_progress"]
        expect_time, expect_progress = expect_progress["time"], expect_progress["percentage"]
        detect_result = self._iteration_time <= expect_time or self._maximum_progress >= expect_progress
        return True if expect_time < 0 else detect_result

    def _is_solver_in_time_limit(self):
        time_limit = self._global_config["time_limit"]
        return True if time_limit < 0 else self._iteration_time <= time_limit

    @staticmethod
    def _generate_global_config():
        return ProjectHelper().get_project_config()["global"]

    def _generate_show_progress_method(self):
        def do_something():
            print("当前进度为: {}/{}".format(len(self._pick_list), self._card_count))

        def do_nothing():
            """do nothing here"""

        return do_something if self._global_config["show_progress"] else do_nothing

    def _get_head_list_for_alive(self, head_list):
        card_type_dict = {index: self._card_container.get_card_detail(index).get_card_type() for index in head_list}
        if self._residual_pool.is_card_type_close_to_limit():
            return []
        elif self._residual_pool.is_pool_count_close_to_limit():
            expect_type_list = self._residual_pool.get_almost_card_type_list()
            match_list = [index for index, current_type in card_type_dict.items() if current_type in expect_type_list]
            return match_list
        elif self._residual_pool.is_card_type_close_to_possible():
            expect_type_list = self._residual_pool.get_all_card_type_list()
            match_list = [index for index, current_type in card_type_dict.items() if current_type in expect_type_list]
            return match_list
        else:
            return head_list

    def _get_head_list_sorted_by_residual(self, head_list):
        card_type_dict = {index: self._card_container.get_card_detail(index).get_card_type() for index in head_list}
        if self._current_progress >= self._global_config["solve_first"]:
            expect_type_list = self._residual_pool.get_sorted_card_type_list()
            return self._sort_head_list_with_type_list(card_type_dict, expect_type_list)
        else:
            return head_list

    @staticmethod
    def _sort_head_list_with_type_list(card_type_dict, type_list):
        result_list = list()
        for type_item in type_list:
            match_list = [index for index, card_type in card_type_dict.items() if card_type == type_item]
            result_list.extend(match_list)
        result_list.extend([index for index in card_type_dict.keys() if index not in result_list])
        return result_list

    def _record_current_progress(self):
        card_list = [item for item in self._pick_list if item != 0]
        self._current_progress = len(card_list) / self._card_count
        if self._current_progress > self._maximum_progress:
            self._maximum_progress = self._current_progress

    def _operation_pick_card(self, card_index):
        self._operation_pool.pick_card(card_index)
        self._residual_pool.pick_card(card_index)
        self._pick_list.append(card_index)

    def _operation_recover_card(self, card_index):
        self._operation_pool.recover_card(card_index)
        self._residual_pool.recover_card(card_index)
        self._pick_list.remove(card_index)

    def generate_card_index_result(self):
        if self._operation_pool.is_game_over():
            return list(self._pick_list)
        else:
            return None

    def generate_card_id_result(self):
        if self._operation_pool.is_game_over():
            card_detail_dict = {index: self._card_container.get_card_detail(index) for index in self._pick_list}
            return [card_detail.get_card_id() for index, card_detail in card_detail_dict.items()]
        else:
            return None

    def generate_card_type_result(self):
        if self._operation_pool.is_game_over():
            card_detail_dict = {index: self._card_container.get_card_detail(index) for index in self._pick_list}
            return {index: card_detail.get_card_type() for index, card_detail in card_detail_dict.items()}
        else:
            return None

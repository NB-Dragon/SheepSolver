#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import time
from core.card.CardSequence import CardSequence
from core.tool.GamePoolController import GamePoolController


class SheepSolver(object):
    def __init__(self, solver_config, solver_algorithm):
        self._stdout_print_method = print
        self._prepare_runtime_param(solver_config, solver_algorithm)

        self._time_distance = []
        self._iteration_time = 0
        self._last_show_time = 0

        self._card_count = 0
        self._current_progress = 0
        self._maximum_progress = 0

    def _prepare_runtime_param(self, solver_config, solver_algorithm):
        self._solver_config = solver_config
        self._card_sequence = CardSequence()
        self._game_pool_controller = GamePoolController(solver_config, solver_algorithm)

    def load_map_data(self, map_data: dict):
        self._game_pool_controller.init_map_data(map_data)
        self._game_pool_controller.prepare_game_data(self._card_sequence)
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
            if self._game_pool_controller.check_fingerprint_exist():
                self._operation_recover_card(head_item)
                continue
            self.solve()
            if not self._game_pool_controller.check_game_over():
                self._operation_recover_card(head_item)
            else:
                break

    def _show_solving_progress(self):
        if self._solver_config["show_progress"] and self._verify_within_time_period(1):
            pick_index_list = self._card_sequence.get_pick_index_list()
            pick_index_list = [item for item in pick_index_list if item >= 0]
            content = "当前进度为: {}/{}".format(len(pick_index_list), self._card_count)
            self._stdout_print_method(content)

    def _verify_within_time_period(self, second):
        if self._iteration_time - self._last_show_time >= second:
            self._last_show_time = self._iteration_time
            return True
        else:
            return False

    def _record_current_progress(self):
        pick_index_list = self._card_sequence.get_pick_index_list()
        pick_index_list = [item for item in pick_index_list if item >= 0]
        self._current_progress = len(pick_index_list) / self._card_count
        if self._current_progress > self._maximum_progress:
            self._maximum_progress = self._current_progress

    def _generate_current_iteration_time(self):
        current_time = time.time()
        if len(self._time_distance) == 2:
            self._time_distance[1] = current_time
            self._iteration_time = self._time_distance[1] - self._time_distance[0]
        else:
            self._time_distance = [current_time, current_time]
            self._iteration_time = 0

    def _check_programme_can_continue(self):
        if self._is_solver_in_time_limit():
            return self._is_solver_progress_meets_expect()
        else:
            return False

    def _is_solver_in_time_limit(self):
        time_limit = self._solver_config["time_limit"]
        return True if time_limit < 0 else self._iteration_time <= time_limit

    def _is_solver_progress_meets_expect(self):
        expect_progress = self._solver_config["expect_progress"]
        expect_time, expect_progress = expect_progress["time"], expect_progress["percentage"]
        detect_result = self._iteration_time <= expect_time or self._maximum_progress >= expect_progress
        return True if expect_time < 0 else detect_result

    def _operation_pick_card(self, card_index):
        self._game_pool_controller.pick_card(card_index)

    def _operation_recover_card(self, card_index):
        self._game_pool_controller.recover_card(card_index)

    def _generate_card_detail_dict(self):
        return self._game_pool_controller.get_all_card_dict()

    @staticmethod
    def _get_card_id_from_detail(card_detail_dict, card_index):
        if card_index in card_detail_dict:
            return card_detail_dict[card_index].get_card_id()
        else:
            return "0-0-0"

    def _generate_card_id_list(self, card_detail_dict, card_list):
        result_list = list()
        for card_item in card_list:
            result_item = self._get_card_id_from_detail(card_detail_dict, card_item)
            result_list.append(result_item)
        return result_list

    @staticmethod
    def _generate_card_type_list(card_list):
        result_list = list()
        for card_item in card_list:
            result_list.append({"index": card_item[0], "type": card_item[1]})
        return result_list

    def generate_card_index_result(self):
        if self._game_pool_controller.check_game_over():
            pick_index_list = self._card_sequence.get_pick_index_list()
            return pick_index_list
        else:
            return None

    def generate_card_id_result(self):
        if self._game_pool_controller.check_game_over():
            card_detail_dict = self._generate_card_detail_dict()
            pick_index_list = self._card_sequence.get_pick_index_list()
            return self._generate_card_id_list(card_detail_dict, pick_index_list)
        else:
            return None

    def generate_card_type_result(self):
        if self._game_pool_controller.check_game_over():
            pick_type_list = self._card_sequence.get_pick_type_list()
            return self._generate_card_type_list(pick_type_list)
        else:
            return None

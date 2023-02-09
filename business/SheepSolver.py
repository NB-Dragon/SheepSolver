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
        head_list = self._operation_pool.get_head_key_list()
        head_list = self._get_head_list_for_alive(head_list)
        if self._get_progress_percentage() >= self._global_config["solve_first"]:
            head_list = self._get_head_list_sorted_by_residual(head_list)
        for head_item in head_list:
            if self._is_solver_time_out():
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

    def _is_solver_time_out(self):
        if self._global_config["time_limit"] < 0:
            return False
        elif isinstance(self._start_time, float):
            time_distance = time.time() - self._start_time
            return time_distance >= self._global_config["time_limit"]
        else:
            self._start_time = time.time()
            return False

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
        expect_type_list = self._residual_pool.get_sorted_card_type_list()
        card_type_dict = {index: self._card_container.get_card_detail(index).get_card_type() for index in head_list}
        result_list = []
        for card_type in expect_type_list:
            match_list = [index for index, current_type in card_type_dict.items() if current_type == card_type]
            result_list.extend(match_list)
        result_list.extend([index for index in head_list if index not in result_list])
        return result_list

    def _get_progress_percentage(self):
        return len(self._pick_list) / self._card_count

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

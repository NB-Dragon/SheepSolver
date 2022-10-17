import json
import os
import sys
from hepler.FileHelper import FileHelper
from item.Card import Card
from item.CardPosition import CardPosition
from item.ResidualPool import ResidualPool


class SheepSolver(object):
    def __init__(self, percentage, sort_mode):
        self._code_entrance_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
        self._origin_data_file = os.path.join(self._code_entrance_path, "online_data.json")
        self._origin_data = FileHelper().read_json_data(self._origin_data_file)
        self._card_count = 0
        self._card_position = CardPosition(sort_mode)
        self._residual_pool = ResidualPool()
        self._pick_list = []
        self._solve_first_percentage = percentage
        self._situation_history = set()

    def init_card_data(self):
        self._origin_data = dict(sorted(self._origin_data.items(), key=lambda item: int(item[0])))
        for level, level_data in self._origin_data.items():
            self._card_count += len(level_data)
            card_list = [Card(item) for item in level_data]
            self._card_position.append_level_card(card_list)
        self._card_position.generate_head_data()

    def solve(self):
        print("当前进度为: {}/{}".format(len(self._pick_list), self._card_count))
        head_list = self._card_position.get_head_key_list()
        head_list = self._get_head_list_for_alive(head_list)
        if len(self._pick_list) / self._card_count >= self._solve_first_percentage:
            head_list = self._get_head_list_sorted_by_residual(head_list)
        for head_item in head_list:
            self._operation_pick_card(head_item)
            head_fingerprint = self._card_position.get_head_description()
            if head_fingerprint in self._situation_history:
                self._operation_recover_card(head_item)
                continue
            else:
                self._situation_history.add(head_fingerprint)
                self.solve()
                if not self._card_position.is_head_data_empty():
                    self._operation_recover_card(head_item)
                else:
                    break

    def _get_head_list_for_alive(self, head_list):
        residual_pool_detail = self._residual_pool.get_pool_detail()
        card_type_dict = {index: self._card_position.get_card_detail(index).get_card_type() for index in head_list}
        if len(residual_pool_detail.keys()) == 6:
            return []
        elif self._residual_pool.get_pool_count() == 6:
            expect_type_list = [card_type for card_type, card_count in residual_pool_detail.items() if card_count == 2]
            match_list = [index for index, current_type in card_type_dict.items() if current_type in expect_type_list]
            return match_list
        elif len(residual_pool_detail.keys()) == 5:
            expect_type_list = list(residual_pool_detail.keys())
            match_list = [index for index, current_type in card_type_dict.items() if current_type in expect_type_list]
            return match_list
        else:
            return head_list

    def _get_head_list_sorted_by_residual(self, head_list):
        residual_pool_detail = self._residual_pool.get_pool_detail()
        residual_pool_detail = dict(sorted(residual_pool_detail.items(), key=lambda a: a[1], reverse=True))
        card_type_dict = {index: self._card_position.get_card_detail(index).get_card_type() for index in head_list}
        result_list = []
        for card_type, card_count in residual_pool_detail.items():
            match_list = [index for index, current_type in card_type_dict.items() if current_type == card_type]
            result_list.extend(match_list)
        result_list.extend([index for index in head_list if index not in result_list])
        return result_list

    def test_result(self, pick_list: list):
        for pick_index in pick_list:
            self._operation_pick_card(pick_index)
            print(self._residual_pool.show_pool_state())

    def _operation_pick_card(self, card_index):
        self._card_position.pick_card(card_index)
        card_detail = self._card_position.get_card_detail(card_index)
        self._residual_pool.pick_card(card_detail)
        self._pick_list.append(card_index)

    def _operation_recover_card(self, card_index):
        self._card_position.recover_card(card_index)
        card_detail = self._card_position.get_card_detail(card_index)
        self._residual_pool.recover_card(card_detail)
        self._pick_list.remove(card_index)

    def print_result(self):
        if self._card_position.is_head_data_empty():
            card_detail_list = [self._card_position.get_card_detail(index) for index in self._pick_list]
            id_list = [item.get_card_id() for item in card_detail_list]
            print(json.dumps(id_list))
        else:
            print("牌面无解")

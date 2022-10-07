import json


class ResidualPool(object):
    def __init__(self):
        # 当前操作池有多少张卡牌
        self._pool_count = 0
        # 当前操作池可容纳的最大牌数
        self._pool_limit = 7
        # 当前操作池帕牌类别及数量
        self._pool_card = {}

    def is_pool_full(self):
        return self._pool_count >= self._pool_limit

    def show_pool_state(self):
        return "count: {}, detail: {}".format(self._pool_count, json.dumps(self._pool_card))

    def pick_card(self, card_detail):
        self._pool_count += 1
        card_type = card_detail.get_type()
        if card_type in self._pool_card:
            self._pool_card[card_type] += 1
        else:
            self._pool_card[card_type] = 1
        self._make_card_disappear(card_type)

    def recover_card(self, card_detail):
        card_type = card_detail.get_type()
        if card_type in self._pool_card:
            if self._pool_card[card_type] == 1:
                self._pool_card.pop(card_type)
            else:
                self._pool_card[card_type] -= 1
            self._pool_count -= 1
        else:
            self._pool_card[card_type] = 2
            self._pool_count += 2

    def _make_card_disappear(self, card_type):
        if self._pool_card[card_type] == 3:
            self._pool_count -= 3
            self._pool_card.pop(card_type)

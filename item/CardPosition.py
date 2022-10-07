class CardPosition(object):
    def __init__(self):
        # 以序号注册所有卡牌数据
        self._origin_data = {}
        # 以序号注册可操作卡牌数据
        self._head_data = {}
        # 当前登记的序号
        self._card_count = 0

    def append_level_card(self, card_list):
        start_index = len(self._origin_data) + 1
        self._append_origin_data(card_list)
        end_index = len(self._origin_data) + 1
        new_card_data = {key: self._origin_data[key] for key in range(start_index, end_index)}
        self._handle_overlap_data(new_card_data)

    def get_head_description(self):
        return "-".join([str(item) for item in sorted(self._head_data.keys())])

    def get_card_detail(self, card_index):
        return self._origin_data[card_index]

    def pick_card(self, card_index):
        self._head_data.pop(card_index)
        children_set = self._origin_data[card_index].get_children_set()
        for children_key in children_set:
            children_item = self._origin_data[children_key]
            children_item.recover_parent(card_index)
            if not children_item.has_parent():
                self._head_data[children_key] = children_item

    def recover_card(self, card_index):
        card_detail = self._origin_data[card_index]
        self._head_data[card_index] = card_detail
        children_set = card_detail.get_children_set()
        for children_key in children_set:
            children_item = self._origin_data[children_key]
            children_item.add_parent(card_index)
            if children_key in self._head_data:
                self._head_data.pop(children_key)

    def get_head_key_list(self):
        return list(self._head_data.keys())

    def is_head_data_empty(self):
        return len(self._head_data.keys()) == 0

    def _append_origin_data(self, card_list):
        for card_item in card_list:
            self._card_count += 1
            self._origin_data[self._card_count] = card_item

    def _handle_overlap_data(self, card_dict):
        overlap_key_set = set()
        for key_new, card_new in card_dict.items():
            for key_old, card_old in self._head_data.items():
                if card_new.clac_iou(card_old) > 0:
                    card_new.add_children(key_old)
                    card_old.add_parent(key_new)
                    overlap_key_set.add(key_old)
        [self._head_data.pop(key) for key in overlap_key_set]
        self._head_data.update(card_dict)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import math
import random


class ShuffleHelper(object):
    def __init__(self, seed_list=None):
        self._seed_1, self._seed_2 = 0, 0
        self._high_number = 2.3283064365386963e-10
        self._low_number = 2.220446049250313e-16
        self._init_random_seed(seed_list)

    def _init_random_seed(self, seed_list):
        if seed_list is not None:
            self._reset_random_seed(seed_list)
            self.get_random()
        else:
            seed_list = self._generate_random_seed()
            self._reset_random_seed(seed_list)

    def _reset_random_seed(self, seed_list):
        self._seed_1 = (seed_list[0] & 0xFFFFFFFF) << 32 | (seed_list[1] & 0xFFFFFFFF)
        self._seed_2 = (seed_list[2] & 0xFFFFFFFF) << 32 | (seed_list[3] & 0xFFFFFFFF)

    def shuffle(self, data_list, iter_limit):
        for i in list(reversed(range(len(data_list))))[0:iter_limit]:
            random_number = self.get_random()
            j = math.floor(random_number * (i + 1))
            data_list[i], data_list[j] = data_list[j], data_list[i]

    def get_random(self):
        random_result = self._get_random_group()
        self._prepare_next_random()
        return self._high_number * random_result[0] + self._low_number * (random_result[1] >> 12)

    def _get_random_group(self):
        result = self._seed_1 + self._seed_2
        return [result >> 32 & 0xFFFFFFFF, result & 0xFFFFFFFF]

    def _prepare_next_random(self):
        seed, self._seed_1 = self._seed_1, self._seed_2
        seed = seed ^ ((seed << 23) & 0xFFFFFFFFFFFFFFFF)
        self._seed_2 = seed ^ self._seed_2 ^ (seed >> 18) ^ (self._seed_2 >> 5)

    @staticmethod
    def _generate_random_seed():
        return [random.randint(0, 0xFFFFFFFF) for item in range(4)]

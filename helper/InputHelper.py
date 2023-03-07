#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import argparse
import time


class InputHelper(object):
    def __init__(self):
        self._expect_list = ["normal", "index", "index-reverse", "level-bottom", "level-top", "random"]
        self._continue_checking = True

    def get_runtime_arguments(self, ):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument("-m", "--mode", dest='mode', required=True, help="The mode to solve game.")
            args = parser.parse_args()
            return args if self._check_input_args(args) else None
        except SystemExit:
            return None

    def _check_input_args(self, args):
        if not self._check_solve_mode_correct(args.mode):
            message = "The solve mode must be [{}]".format("|".join(self._expect_list))
            self._send_error_message(message)
        return self._continue_checking

    def _check_solve_mode_correct(self, solve_mode):
        return solve_mode in self._expect_list

    def _send_error_message(self, message):
        self._continue_checking = False
        self._make_message_and_send(message)

    @staticmethod
    def _make_message_and_send(content):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        output_content = "[{}][{}]: {}".format(current_time, "ParserHelper", content)
        print(output_content)

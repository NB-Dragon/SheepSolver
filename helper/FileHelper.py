#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2022/11/30 00:00
# Create User: NB-Dragon
import json


class FileHelper(object):
    def read_json_data(self, file_path):
        bytes_data = self.read_bytes_data(file_path) or b"null"
        file_string = bytes_data.decode("utf-8", "surrogatepass")
        return json.loads(file_string)

    def write_json_data(self, file_path, json_data):
        file_string = json.dumps(json_data)
        bytes_data = file_string.encode("utf-8", "surrogatepass")
        self.write_bytes_data(file_path, bytes_data)

    @staticmethod
    def read_bytes_data(file_path):
        try:
            reader = open(file_path, "rb")
            content = reader.read()
            reader.close()
            return content
        except Exception as e:
            return None

    @staticmethod
    def write_bytes_data(file_path, content):
        try:
            writer = open(file_path, "wb")
            writer.write(content)
            writer.close()
        except Exception as e:
            return None

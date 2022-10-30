import json
import os


class FileHelper(object):
    def read_json_data(self, file_path):
        file_content = self.read_file_content(file_path) or "null"
        return json.loads(file_content)

    def write_json_data(self, file_path, json_data):
        json_content = json.dumps(json_data)
        self.write_file_content(file_path, json_content)

    @staticmethod
    def read_file_content(file_path):
        try:
            if os.path.exists(file_path):
                reader = open(file_path, "r")
                content = reader.read()
                reader.close()
                return content
            else:
                return None
        except Exception as e:
            return None

    @staticmethod
    def write_file_content(file_path, content):
        try:
            writer = open(file_path, "w")
            writer.write(content)
            writer.close()
        except Exception as e:
            print("文件写入失败: {}, 出错详情为: {}".format(file_path, str(e)))

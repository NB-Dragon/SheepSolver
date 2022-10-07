import json
import os.path


class FileHelper(object):
    def read_json_data(self, file_path):
        file_content = self.read_file_content(file_path) or "null"
        return json.loads(file_content)

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

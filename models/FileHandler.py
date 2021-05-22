import json
import os


class FileHandler:
    def read(self):
        pass

    def write(self):
        pass


class TxtFileHandler(FileHandler):
    def read(self, file_name: str) -> str:
        file = open(file_name, 'r')
        data = file.read()
        file.close()
        return data


class JSONFileHandler(FileHandler):
    def read(self, file_name: str):
        if os.path.isfile(file_name):
            file = open(file_name, 'r')
            data = json.load(file)
            file.close()
            return data
        else:
            return {}

    def write(self, data: dict, filename):
        json_data = json.dumps(data)
        if os.path.isfile(filename):
            file = open(filename, 'w')
            file.write(json_data)
            file.close()
        else: 
            file = open(filename, 'x')
            file.write(json_data)
            file.close()


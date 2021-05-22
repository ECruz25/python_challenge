import datetime
from models.FileHandler import JSONFileHandler

class Cache:
    expire_after = 180
    name = ''

    def __init__(self, name: str, expire_after:int=180):
        self.expire_after = expire_after
        self.name = name

    def read(self) -> dict:
        return {}

    def write(self):
        pass


def write_expiring_date_time(json, expire_after):
    date_to_expire = (datetime.datetime.now() + datetime.timedelta(0, expire_after)).strftime("%m-%d-%Y %H:%M:%S")
    if 'expiring_date' in json:
        return json
    json['expiring_date'] = date_to_expire
    return json

def expiration_checker(date):
    date = datetime.datetime.strptime(date, "%m-%d-%Y %H:%M:%S")
    return datetime.datetime.now() < date


class JSONCache(Cache):
    def read(self) -> dict:
        filename = f'{self.name}_cache.json'
        json_handler = JSONFileHandler()
        data = json_handler.read(filename)
        unexpired_data = {key: data[key] for key in data if expiration_checker(data[key]['expiring_date'])}
        return unexpired_data

    def write(self, new_data):
        filename = f'{self.name}_cache.json'
        previous_data = self.read()
        data = {**previous_data, **new_data}
        data_with_expiring_date = {key : write_expiring_date_time(data[key], self.expire_after) for key in data}
        json_handler = JSONFileHandler()
        json_handler.write(data_with_expiring_date, filename)


class JSONCacheVerifier:
    def exists(self, value, cache: Cache):
        return value in cache.read()



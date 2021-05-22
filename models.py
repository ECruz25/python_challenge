import re
import requests
import datetime
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



class Parser:
    value_to_parse = ''

    def __init__(self, value_to_parse: str):
        self.value_to_parse = value_to_parse

    def parse(self):
        pass


class IPParser(Parser):
    def parse(self) -> list[str]:
        ips = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', self.value_to_parse)
        return ips


class IPListData:
    list_of_ips = []
    def __init__(self, list_of_ips: list[str]):
        self.list_of_ips = list_of_ips

    def get_data(self):
        return []

class IpListGeoLocation(IPListData):
    def get_data(self):
        api_url = 'http://ipwhois.app/json/'
        data = []
        http_handler = HTTPHandler()
        for ip_address in self.list_of_ips:
            response = http_handler.get(f'{api_url}{ip_address}')
            data.append(response)
        return data


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


class HTTPHandler:
    def get(self, url, params=None, headers=None):
        cache = JSONCache('http_get', 60)
        exists_in_cache = JSONCacheVerifier().exists(url, cache)
        if exists_in_cache:
            return cache.read()[url]
        response = requests.get(url, params=params, headers=headers)
        ip_geo_location = response.json()
        data_to_cache = {
            url: ip_geo_location
        }
        cache.write(data_to_cache)
        return ip_geo_location

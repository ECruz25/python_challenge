from models.HTTPHandler import HTTPHandler


class IPListData:
    list_of_ips = []
    def __init__(self, list_of_ips: list[str]):
        self.list_of_ips = list_of_ips

    def get_data(self):
        return []

class IpListGeoLocation(IPListData):
    url = 'http://ipwhois.app/json/'
    def get_data(self):
        data = []
        http_handler = HTTPHandler()
        for ip_address in self.list_of_ips:
            response = http_handler.get(f'{self.url}{ip_address}')
            data.append(response)
        return data

class IPListRDAPLookUp(IPListData):
    url = 'https://rdap.arin.net/registry/ip/'
    def get_data(self):
        data = []
        http_handler = HTTPHandler()
        for ip_address in self.list_of_ips:
            response = http_handler.get(f'{self.url}{ip_address}')
            data.append(response)
        return data
import re

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

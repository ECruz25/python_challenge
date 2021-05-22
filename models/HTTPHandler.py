import requests
from models.Cache import JSONCache, JSONCacheVerifier

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

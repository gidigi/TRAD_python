import http.client
from urllib.parse import urlparse
import json


class redmine:
    def __init__(self):
        self.__protocol = "http"
        self.__port     = 80
        self.__url      = "127.0.0.1"
        self.__auth     = "null"
        self.__conn     = ""
        self.__head     = {}
    def __headers(self):
        out = {
            'Content-type' : 'application/json;charset=utf-8',
            'User-Agent'   : 'Mozilla/5.0 hyper0 openBSD'
        }
        for name, value in self.__head.items():
            out[name] = value

        out["X-Redmine-API-Key"] = self.__auth
        return out;
    def setup(self, url, auth):
        parts           = urlparse(url)
        self.__url      = parts.hostname
        self.__port     = parts.port
        self.__portocol = parts.scheme
        self.__auth     = auth
        self.setHttp()
    def setHttp(self):
        if self.__protocol == 'http':
            self.__conn = http.client.HTTPConnection(
                self.__url, 
                self.__port
            )
        else:
            self.__conn = http.client.HTTPConnection(
                self.__url, 
                self.__port
            )
    def __get(self, url: str)->tuple:
        self.__conn.request('GET', url, '', self.__headers()) 
        response = self.__conn.getresponse()
        self.__last_response = response
        if response.status == 200:
            return response.read().decode()
    def projects(self)->dict:
        result = json.loads(self.__get('/projects.json'))
        return result
    def trackers(self)->dict:
        result = json.loads(self.__get('/trackers.json'))
        return result
    def issues(self)->dict:
        result = json.loads(self.__get('/issues.json?limit=100'))
        return result

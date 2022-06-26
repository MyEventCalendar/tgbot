"""Работа с API методами"""
import json
import urllib3
from . settings import API_URL

http = urllib3.PoolManager()


class ApiController():
    def __init__(self):
        self.__response_data__ = None
        self._headers = None

    def make_headers(self, telegram_id, password):
        self._headers = urllib3.make_headers(basic_auth=f"{telegram_id}:{password}")
        return self._headers

    def get_all_events(self):
        """Get-запрос, возвращает список всех событий хранящихся в БД"""
        response = http.request("GET", f"{API_URL}/events/", headers=self._headers)
        self.__response_data__ = response.data
        return self.__parse_data__()

    def get_actual_events(self):
        """Get-запрос, возвращает список всех актуальных событий хранящихся в БД"""
        response = http.request("GET", f"{API_URL}/events/", headers=self._headers)
        self.__response_data__ = response.data
        return self.__parse_data__()

    def delete_event(self, pk):
        """Delete-запрос, удаляет событие из БД по его ID"""
        response = http.request("DELETE", f"{API_URL}/events/{pk}", headers=self._headers)
        self.__response_data__ = response.data
        return self.__parse_data__()

    def post_event(self, payload):
        """Post-запрос, сохраняет новое событие в БД"""
        response = http.request("POST", f"{API_URL}/events/", fields=payload,  headers=self._headers)
        self.__response_data__ = response.data
        return self.__parse_data__()

    def put_change_event(self, pk, payload):
        """Put-запрос, изменяет уже существующее событие в БД"""
        response = http.request("PUT", f"{API_URL}/events/{pk}", fields=payload, headers=self._headers)
        self.__response_data__ = response.data
        return self.__parse_data__()

    def post_user(self, payload):
        """Post-запрос, сохраняет нового пользователя в БД"""
        response = http.request("POST", f"{API_URL}/users/", fields=payload)
        self.__response_data__ = response.data
        return self.__parse_data__()

    def __parse_data__(self):
        return json.loads(self.__response_data__.decode("utf-8"))

"""Модуль подключение к Smartis API."""


import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from .exceptions import ErrorMessages, SmartisAPIError

load_dotenv()


class HttpRequester(ABC):
    """Класс абстракции для HTTP запросов."""

    @abstractmethod
    def make_request(self, url, method, headers, data):
        """Обработка запросов к API."""
        pass


@dataclass
class DefaultHttpRequester(HttpRequester):
    """Дефолтная конфигурация для HttpRequester."""

    session = requests.Session()

    def make_request(self, url, method, headers, data):
        """
        Обработка запроса к эндпоинту.

        Включая роутинг типов запросов в зависимости от метода обращения и
        обработка исключений/ошибок взаимодействия с энедпоинтами Smartis API.
        """
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers)
            else:
                response = self.session.post(url, headers=headers, json=data)

            response.raise_for_status()

        except requests.exceptions.ConnectionError as e:
            raise SmartisAPIError(str(e))

        except requests.exceptions.RequestException as re:
            error_message = ErrorMessages.get_error_message(response, re)
            raise SmartisAPIError(error_message)

        try:
            return response.json()

        except requests.exceptions.JSONDecodeError:
            error_message = ErrorMessages.get_json_decode_error_message(
                response
            )
            raise SmartisAPIError(error_message)


@dataclass
class SmartisAPIClient:
    """Подключение к Smartis API."""

    BASE_URL: str = "https://my.smartis.bi/api"
    API_KEY: str = os.getenv("API_TOKEN")
    http_requester: HttpRequester = DefaultHttpRequester()
    headers = {"Authorization": f"Bearer {API_KEY}"}

    def _make_request(self, endpoint, method="POST", data=None):
        """Отправка запроса на эндпоинт API."""
        if self.API_KEY is None:
            raise ValueError("API_TOKEN is not set.")

        url = f"{self.BASE_URL}{endpoint}"
        return self.http_requester.make_request(
            url, method, self.headers, data
        )


class SmartisAPIEndpoints(SmartisAPIClient):
    """Эндпоинты Smartis API."""

    def get_report(self, payload):
        """Эндпоинт /reports/getReport."""
        endpoint = "/reports/getReport"
        return self._make_request(endpoint, data=payload)

    def get_keywords(self, payload):
        """Эндпоинт /reports/getKeywords."""
        endpoint = "/reports/getKeywords"
        return self._make_request(endpoint, data=payload)

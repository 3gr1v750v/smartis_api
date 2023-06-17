import http.client
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from .exceptions import SmartisAPIError

load_dotenv()


class HttpRequester(ABC):
    """Класс абстракции для HTTP запросов."""

    @abstractmethod
    def make_request(self, url, method, headers, data):
        """Обработка запросов к API."""
        pass


class DefaultHttpRequester(HttpRequester):
    """Дефолтная конфигурация для HttpRequester."""

    def make_request(self, url, method, headers, data):
        """
        Обработка запроса к эндпоинту. Включая роутинг типов запросов
        в зависимости от метода обращения и обработка исключений/ошибок
        взаимодействия с энедпоинтами Smartis API.
        """
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, headers=headers, json=data)

            response.raise_for_status()

        except requests.exceptions.ConnectionError as e:
            return str(e)

        except requests.exceptions.RequestException as e:
            error_message = response.content.decode("unicode_escape")
            status_code_name = http.client.responses.get(
                response.status_code, "Unknown"
            )
            error_type = type(e).__name__
            raise SmartisAPIError(
                f"{error_type} - {response.status_code} "
                f"{status_code_name}\n{error_message}"
            )

        return response.json()


@dataclass
class SmartisAPIClient:
    """Подключение к Smartis API."""

    BASE_URL: str = "https://my.smartis.bi/api"
    API_KEY: str = os.getenv("API_TOKEN")
    http_requester: HttpRequester = DefaultHttpRequester()

    def _make_request(self, endpoint, method="POST", data=None):
        """Отправка запроса на эндпоинт API."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {self.API_KEY}"}

        return self.http_requester.make_request(url, method, headers, data)


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

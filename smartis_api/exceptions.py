"""Обработка ошибок обращения к Smartis API."""

import http.client


class SmartisAPIError(Exception):
    """Обработка исключений обращения к эндпоинтам Smartis API."""

    pass


class ErrorMessages:
    """Обработка текста ошибок при работе с API."""

    @staticmethod
    def get_error_message(response, error_code):
        """Обаботка стандартных ошибок работы эндпоинта."""
        error_message = response.content.decode("unicode_escape")
        status_code_name = http.client.responses.get(
            response.status_code, "Unknown"
        )
        error_type = type(error_code).__name__
        return (
            f"{error_type} - {response.status_code} "
            f"{status_code_name}: {error_message}"
        )

    @staticmethod
    def get_json_decode_error_message(response):
        """Обработка ошибки связанной с JSON представлением ответа API."""
        status_code_name = http.client.responses.get(
            response.status_code, "Unknown"
        )
        error = {
            "error": "API response could not be parsed in JSON format. "
            "Possible error source: - API Token is incorrect "
            "or missing."
        }
        return f"{response.status_code} {status_code_name}: {error}"

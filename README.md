# Пакет для подключения к Smartis API.

## Описание проекта.
Реализация пакета для подключения к эндпоинтам Smartis API (https://my.smartis.bi/). Архитектурное решение
содержит примеры подключение к двум эндпоинтам: "/reports/getReport" и 
"/reports/getKeywords". Подключение к остальным эндпоинтам Smartis API может
быть реализовано аналогично текущему паттерну в классе SmartisAPIEndpoints (api_client.py).

Проект включает тесты для вышеуказанных эндпоинтов, для проверки ответов API
для дефолтных запросов при работе с демонстрационным API Токеном.

В основном исполняемом файле проекта (main.py) предоставлен пример использования
пакета smartis_api на примере к эндпоинту "/reports/getReport".

## Установка и запуск (локальный).

1. Скопируйте репозиторий и перейдите в него в командной строке:

```
git clone git@github.com:3gr1v750v/smartis_api.git
```

```
cd smartis_api
```

2. Создайте и активируйте виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

3. Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Создайте '.env' фаил в директории "smartis_api":

Демо-токен предоставлен в  документации Smartis API (https://my.smartis.bi/api/documentation)

```
API_TOKEN = <your_api_token_here>
```

5. Если вы используете демо-токен, можете запустить тесты проверки работы эндпоинтов:

```
python -m tests.smartis_api_endpoints_test
```

5. Запустите проект:

```
python main.py
```
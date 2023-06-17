import json

from smartis_api import SmartisAPIEndpoints, SmartisAPIError


def main():
    """Управление обращения к эндпоинтам через пакет smartis_api."""

    client = SmartisAPIEndpoints()

    try:
        payload = {
            "project": "object_282",
            "metrics": "vse-obrascheniya-novyy-_1508235518;comagic_calls;"
                       "crm_contracts",
            "datetimeFrom": "2020-01-01 00:00:00",
            "datetimeTo": "2020-01-31 23:59:59",
            "groupBy": "day",
            "type": "aggregated",
            "filters": [
                {
                    "filter_category": 1,
                    "filter_condition": ">=",
                    "filter_value": "60",
                }
            ],
            "attribution": {
                "model_id": 1,
                "period": "90",
                "with_direct": True,
            },
            "fields": [["utm_source", "id"]],
            "topCount": 250,
        }

        report = client.get_report(payload)

        formatted_data = json.dumps(report, indent=4, ensure_ascii=False)
        print(formatted_data)

    except SmartisAPIError as e:
        print(str(e))


if __name__ == "__main__":
    main()

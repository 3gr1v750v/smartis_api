import unittest
from unittest.mock import patch

from smartis_api import SmartisAPIEndpoints


class TestSmartisAPIEndpoints(unittest.TestCase):
    @patch("requests.request")
    def test_get_report_default(self, mock_request):
        """
        Проверка соответствия дефолтного запроса и ответа эндпоинта
        /reports/getReport.
        """
        api_reports = SmartisAPIEndpoints()
        response = api_reports.get_report(
            {
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
                "topCount": 251,
            }
        )

        self.assertEqual(
            response["reports"]["vse-obrascheniya-novyy-_1508235518"][
                "20200101"
            ],
            6,
        )
        self.assertEqual(
            response["reports"]["vse-obrascheniya-novyy-_1508235518"][
                "20200102"
            ],
            8,
        )
        self.assertEqual(response["reports"]["comagic_calls"]["20200101"], 5)
        self.assertEqual(response["reports"]["comagic_calls"]["20200102"], 7)
        self.assertEqual(response["reports"]["crm_contracts"]["20200101"], 7)
        self.assertEqual(response["reports"]["crm_contracts"]["20200102"], 5)

    @patch("requests.request")
    def test_get_keywords_default(self, mock_request):
        """
        Проверка соответствия дефолтного запроса и ответа эндпоинта
        /reports/getKeywords.
        """
        api_reports = SmartisAPIEndpoints()
        response = api_reports.get_keywords({"ids": [6042837, 6042753]})

        expected_keywords = [
            {"id": 6042753, "keyword": "жк с отделкой под ключ в москве"},
            {
                "id": 6042837,
                "keyword": "однокомнатная квартира в свао купить недорого|"
                "kwid_39977193947",
            },
        ]

        self.assertEqual(response["keywords"], expected_keywords)


if __name__ == "__main__":
    unittest.main()

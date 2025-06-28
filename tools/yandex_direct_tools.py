"""
Инструменты для работы с API Яндекс.Директ.
"""
# region Импорты
from typing import List, Optional, Dict, Any
import uuid
import datetime
from time import sleep
import requests
from requests.exceptions import HTTPError
from logger.logger_config import setup_logger
import pandas as pd
import os
# endregion

# region Логгер
logger = setup_logger(__name__)
# endregion

# region Константы
API_V4_URL = "https://api.direct.yandex.ru/live/v4/json/"
API_V5_URL = "https://api.direct.yandex.com/json/v5/"
# endregion

# region Вспомогательные классы
class APIv5RequestHandler:
    @staticmethod
    def send_request(url: str, headers: dict, params: dict) -> requests.Response:
        response = requests.post(url, headers=headers, json=params)
        response.encoding = "utf-8"
        if response.status_code == 200:
            if "error" in response.json():
                raise HTTPError(
                    f"Ошибка валидации! Код: {response.json()['error']['error_code']}. Текст: {response.json()['error']['error_detail']}"
                )
            return response
        elif response.status_code in (201, 202):
            return response
        elif response.status_code in (400, 404):
            raise HTTPError(
                f"Ошибка валидации! Код: {response.json()['error']['error_code']}. Текст: {response.json()['error']['error_detail']}"
            )
        else:
            raise HTTPError(
                f"Ошибка при выполнении запроса: {response.json()['error']['error_code']}"
            )

class APIv5StatisticsRequestHandler:
    @staticmethod
    def send_request(url: str, headers: dict, params: dict) -> requests.Response:
        response = requests.post(url, headers=headers, json=params)
        response.encoding = "utf-8"
        if response.status_code in (200, 201, 202):
            return response
        elif response.status_code in (400, 404):
            raise HTTPError(
                f"Ошибка валидации! Код: {response.json()['error']['error_code']}. Текст: {response.json()['error']['error_detail']}"
            )
        else:
            raise HTTPError(
                f"Ошибка при выполнении запроса: {response.json()['error']['error_code']}"
            )

class APIv4RequestHandler:
    @staticmethod
    def send_request(url: str, params: dict) -> dict:
        response = requests.post(url, json=params)
        response.encoding = "utf-8"
        if response.status_code in (200, 201, 202):
            return response.json()
        elif response.status_code in (400, 404):
            raise HTTPError(
                f"Ошибка в ответе сервера! Код: {response.json()['error_str']['error_code']}"
            )
        else:
            raise HTTPError(
                f"Ошибка в ответе сервера! Код: {response.json()['error_str']['error_code']}"
            )
# endregion

# region Основные функции API

def get_account_balance(api_token: str, login: str, include_vat: bool = False) -> pd.DataFrame:
    """
    Получает баланс аккаунта Яндекс.Директ.
    Args:
        api_token: OAuth-токен.
        login: Логин пользователя.
        include_vat: Включать ли НДС в сумму.
    Returns:
        pd.DataFrame: Баланс аккаунта.
    """
    params = {
        "method": "AccountManagement",
        "token": api_token,
        "locale": "ru",
        "param": {"Action": "Get"},
    }
    api_response_login = login.replace(".", "-")
    logger.debug(f"Логин на входе: {login}")
    response_data = APIv4RequestHandler.send_request(API_V4_URL, params)
    if response_data.get("data", {}).get("Accounts") == []:
        error = response_data["data"]["ActionsResult"][0]["Errors"][0]
        logger.error(f"Ошибка в названии клиента: {error['FaultString']}")
        raise ValueError(f"Ошибка в названии клиента: {error['FaultString']}")
    if (
        response_data.get("error_detail") == "Поле SelectionCriteria должно быть указано"
        or response_data.get("data", {}).get("Accounts", [{}])[0].get("Login") != api_response_login
    ):
        params["param"]["SelectionCriteria"] = {"Logins": [login]}
        response_data = APIv4RequestHandler.send_request(API_V4_URL, params)
    logger.debug(f"Ответ от сервера: {response_data}")
    actions_result = response_data.get("data", {}).get("ActionsResult", [])
    if actions_result and actions_result[0].get("Errors"):
        error = actions_result[0]["Errors"][0]
        raise ValueError(
            f"Ошибка в названии клиента: {error.get('FaultString', 'Неизвестная ошибка')} (Код: {error.get('FaultCode', 'неизвестен')})"
        )
    raw_budget_value = response_data["data"]["Accounts"][0]["Amount"]
    try:
        float_budget_value = float(raw_budget_value)
    except Exception:
        raise ValueError(r"Ошибка при попытке перевести бюджет во float!")
    if include_vat:
        float_budget_value *= 1.2
    return pd.DataFrame([{"Budget": float_budget_value}])

def get_statistics(
    login: str,
    api_token: str,
    date_from: str,
    date_to: str,
    goals: list[int],
    attribution_models: list[str],
    field_names: list[str],
    report_type: str,
    include_vat: bool,
) -> list[dict]:
    """
    Получает статистику по кампаниям/группам/объявлениям Яндекс.Директ за указанный период.

    Args:
        login: Логин пользователя в Яндекс.Директ.
        api_token: OAuth-токен для доступа к API.
        date_from: Начальная дата (YYYY-MM-DD).
        date_to: Конечная дата (YYYY-MM-DD).
        goals: Список ID целей Яндекс.Метрики.
        attribution_models: Список моделей атрибуции.
        field_names: Список полей для отчёта.
        report_type: Тип отчёта (например, "CAMPAIGN_PERFORMANCE_REPORT").
        include_vat: Включать ли НДС в суммы.

    Returns:
        list[dict]: Список строк отчёта (dict по полям field_names).
    """
    url = API_V5_URL + "reports"
    headers = {
        "Accept-Language": "ru",
        "processingMode": "auto",
        "returnMoneyInMicros": "false",
        "skipReportHeader": "true",
        "skipReportSummary": "true",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
        "Client-Login": login,
    }
    offset = 0
    all_data = []
    chunk_size = 50000
    report_name = str(uuid.uuid4())
    while True:
        params = {
            "params": {
                "SelectionCriteria": {"DateFrom": date_from, "DateTo": date_to},
                "Goals": goals,
                "AttributionModels": attribution_models,
                "FieldNames": field_names,
                "Page": {"Limit": chunk_size, "Offset": offset},
                "ReportName": report_name,
                "ReportType": report_type,
                "DateRangeType": "CUSTOM_DATE",
                "Format": "TSV",
                "IncludeVAT": "YES" if include_vat else "NO",
            }
        }
        response = APIv5StatisticsRequestHandler.send_request(url, headers, params)
        if response.status_code == 200:
            data = _transform_stat_data_to_list_of_dict(response.text)
            all_data.extend(data)
            if len(data) < chunk_size:
                break
            offset += chunk_size
            report_name = str(uuid.uuid4())
        else:
            logger.debug("Данные еще не готовы. Жду 5 секунд.")
            sleep(5)
            continue
    return all_data
# endregion

# region Вспомогательные функции

def _transform_stat_data_to_list_of_dict(tsv_data: str) -> List[Dict[str, Any]]:
    lines = tsv_data.strip().split("\n")
    headers = lines[0].split("\t")
    data = []
    for line in lines[1:]:
        values = line.split("\t")
        row = {header: value for header, value in zip(headers, values)}
        data.append(row)
    return data
# endregion 
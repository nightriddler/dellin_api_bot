import json
import logging
import pprint
from http import HTTPStatus
from typing import Any, Optional

import requests
from contains import DELLIN_APPKEY, DELLIN_LOGIN, DELLIN_PASSWORD


class DellinApi:
    host = "https://api.dellin.ru"
    url_login = f"{host}/v3/auth/login.json"
    url_contragents = f"{host}/v2/counteragents.json"
    url_orders = f"{host}/v3/orders.json"
    url_order_history = f"{host}/v3/orders/statuses_history.json"
    headers = {"Content-type": "application/json"}

    def __init__(
        self, appKey: str, login: Optional[str] = None, password: Optional[str] = None
    ):
        self.appKey = appKey
        self.sessionID = None
        if login and password:
            self._auth(login, password)

    def _auth(self, login: str, password: str):
        auth_data = {
            "login": login,
            "password": password,
        }
        auth_data.update(self._public_auth())
        r = requests.post(
            self.url_login, data=json.dumps(auth_data), headers=self.headers
        )
        self.sessionID = r.json()["data"]["sessionID"]

    def _public_auth(self) -> dict[str, str]:
        return {
            "appKey": self.appKey,
        }

    def _customers_auth(self) -> dict[str, str]:
        return {
            "appKey": self.appKey,
            "sessionID": self.sessionID,
        }

    def get_counteragents(self) -> Any:
        """Запрос на страницу контрагентов."""
        data = self._customers_auth()
        fullinfo = {"fullinfo": True}
        data.update(fullinfo)

        try:
            logging.info(f"Старт запроса на страницу {self.url_contragents}.")
            response = requests.post(
                self.url_contragents,
                data=json.dumps(data),
                headers=self.headers,
            )
            if response.status_code != HTTPStatus.OK:
                logging.error(f"Получен статус код: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе контрагента: {e}")

        logging.info(f"Успешный запрос на страницу {self.url_contragents}.")
        return response.json()

    def get_orders(self) -> Any:
        """
        Запрос на страницу журнала заказов.
        Сортировка заказов по дате обновления.
        """
        data = self._customers_auth()
        fullinfo = {"orderBy": "ordered_at"}
        data.update(fullinfo)

        try:
            logging.info(f"Старт запроса на страницу {self.url_orders}.")
            response = requests.post(
                self.url_orders,
                data=json.dumps(data),
                headers=self.headers,
            )
            if response.status_code != HTTPStatus.OK:
                logging.error(f"Получен статус код: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе контрагента: {e}")

        logging.info(f"Успешный запрос на страницу {self.url_orders}.")
        return response.json()

    def get_order_history(self, id: str) -> Any:
        """
        Запрос на страницу страницу заказа.
        Содержит информацию о перемещении груза.
        """
        data = self._public_auth()
        fullinfo = {"docIds": [id]}
        data.update(fullinfo)

        try:
            logging.info(f"Старт запроса на страницу {self.url_order_history}.")
            response = requests.post(
                self.url_order_history,
                data=json.dumps(data),
                headers=self.headers,
            )
            if response.status_code != HTTPStatus.OK:
                logging.error(f"Получен статус код: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе контрагента: {e}")

        logging.info(f"Успешный запрос на страницу {self.url_order_history}.")
        return response.json()


dl = DellinApi(
    DELLIN_APPKEY,
    login=DELLIN_LOGIN,
    password=DELLIN_PASSWORD,
)

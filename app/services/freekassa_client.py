import os
import hashlib
import time
import requests
from freekassa import FreeKassaApi

from app.utils.freekassa_exceptions import FreekassaApiError, FreekassaAuthError, FreekassaValidationError


class FreeKassaClient:
    def __init__(self):
        self.merchant_id = os.getenv("FREEKASSA_MERCHANT_ID")
        self.secret_word = os.getenv("FREEKASSA_SECRET_WORD")  # Для формирования ссылки
        self.secret_word_2 = os.getenv("FREEKASSA_SECRET_WORD2")  # Для проверки webhook-а
        self.api_key = os.getenv("FREEKASSA_API_KEY", "")  # API ключ для дополнительных методов
        self.wallet_id = os.getenv("FREEKASSA_WALLET_ID", "")  # ID кошелька для работы с API
        
        # Базовый URL для API FreeKassa
        self.api_base_url = "https://api.freekassa.ru/v1"
        
        # Инициализация API клиента для базовых функций
        self.api_client = FreeKassaApi(
            first_secret=self.secret_word,
            second_secret=self.secret_word_2,
            merchant_id=self.merchant_id,
            wallet_id=self.wallet_id
        )

    def create_payment_url(self, amount: int, order_id: int, description: str, currency="RUB", email=None):
        """
        Создает URL для оплаты
        :param amount: сумма в копейках
        :param order_id: идентификатор заказа
        :param description: описание платежа
        :param currency: валюта платежа
        :param email: email плательщика (опционально)
        :return: URL для перехода на страницу оплаты
        """
        try:
            amount_rub = amount / 100  
            
            # Используем библиотеку для генерации ссылки
            return self.api_client.generate_payment_link(
                order_id=str(order_id),
                summ=amount_rub,
                email=email,
                description=description
            )
        except Exception as e:
            raise FreekassaApiError(f"Ошибка при создании ссылки на оплату: {str(e)}")
    
    def check_payment_status(self, order_id: str, int_id: str = None):
        """
        Проверяет статус платежа
        :param order_id: ID заказа в системе
        :param int_id: Внутренний ID платежа (опционально)
        :return: Информация о платеже
        """
        try:
            return self.api_client.get_order(order_id, int_id)
        except Exception as e:
            raise FreekassaApiError(f"Ошибка при проверке статуса платежа: {str(e)}")
    
    def get_balance(self):
        """
        Получает баланс аккаунта FreeKassa
        :return: Информация о балансе
        """
        try:
            return self.api_client.get_balance()
        except Exception as e:
            raise FreekassaApiError(f"Ошибка при получении баланса: {str(e)}")
    
    def export_orders(self, status=None, date_from=None, date_to=None, limit=100, offset=0):
        """
        Экспортирует список заказов
        :param status: Статус заказов (успешные, отмененные, все)
        :param date_from: Начальная дата (формат YYYY-MM-DD)
        :param date_to: Конечная дата (формат YYYY-MM-DD)
        :param limit: Лимит выборки
        :param offset: Смещение выборки
        :return: Список заказов
        """
        try:
            return self.api_client.export_order(status, date_from, date_to, limit, offset)
        except Exception as e:
            raise FreekassaApiError(f"Ошибка при экспорте заказов: {str(e)}")
    
    def _generate_signature(self, data):
        """
        Генерирует подпись для запросов к API
        :param data: Словарь с данными запроса
        :return: Подпись запроса
        """
        # Сортировка параметров по ключу
        sorted_params = sorted(data.items(), key=lambda x: x[0])
        
        # Формирование строки для подписи
        string_to_sign = "".join([str(value) for _, value in sorted_params]) + self.api_key
        
        # Хэширование строки в MD5
        signature = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest()
        
        return signature
    
    def _make_api_request(self, endpoint, params=None):
        """
        Выполняет запрос к API FreeKassa
        :param endpoint: Эндпоинт API
        :param params: Параметры запроса (опционально)
        :return: Ответ от API
        """
        url = f"{self.api_base_url}/{endpoint}"
        
        if params is None:
            params = {}
            
        # Добавляем обязательные параметры
        data = {
            "shopId": self.merchant_id,
            "nonce": int(time.time()),
            **params
        }
        
        # Генерируем подпись запроса
        signature = self._generate_signature(data)
        data["signature"] = signature
        
        # Выполняем запрос к API
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            response_data = response.json()
            
            # Проверяем ответ на наличие ошибок
            if response_data.get("type") == "error":
                error_msg = response_data.get("message", "Неизвестная ошибка")
                error_code = response_data.get("code", 0)
                
                if error_code == 401:
                    raise FreekassaAuthError(error_msg, error_code)
                elif error_code == 400:
                    raise FreekassaValidationError(error_msg, error_code, response_data.get("errors"))
                else:
                    raise FreekassaApiError(error_msg, error_code)
                    
            return response_data
        except requests.exceptions.RequestException as e:
            raise FreekassaApiError(f"Ошибка сетевого запроса: {str(e)}")
        
    def get_payment_systems(self):
        """
        Получает список доступных платежных систем
        :return: Список платежных систем в формате:
        {
            "type": "success",
            "currencies": [
                {
                    "id": 4,
                    "name": "VISA",
                    "currency": "RUB",
                    "is_enabled": 1,
                    "is_favorite": 0
                }
            ]
        }
        """
        return self._make_api_request("currencies")
        
    def check_payment_system(self, payment_system_id: int):
        """
        Проверяет доступность платежной системы
        :param payment_system_id: ID платежной системы
        :return: Статус доступности в формате:
        {
            "type": "success"
        }
        """
        return self._make_api_request(f"currencies/{payment_system_id}/status")
        
    def get_payment_systems_for_withdrawal(self):
        """
        Получает список доступных платежных систем для вывода
        :return: Список платежных систем для вывода в формате:
        {
            "type": "success",
            "currencies": [
                {
                    "id": 4,
                    "name": "VISA",
                    "min": 100,
                    "max": 15000,
                    "currency": "RUB",
                    "can_exchange": 1
                }
            ]
        }
        """
        return self._make_api_request("withdrawals/currencies")
        
    def get_shops(self):
        """
        Получает список доступных магазинов
        :return: Список магазинов в формате:
        {
            "type": "success",
            "shops": [
                {
                    "id": 777,
                    "name": "Название магазина",
                    "url": "https://example.com"
                }
            ]
        }
        """
        return self._make_api_request("shops")
        
    def create_withdrawal(self, payment_system_id: int, account: str, amount: float, 
                         currency: str = "RUB", payment_id: str = None):
        """
        Создает выплату
        :param payment_system_id: ID платежной системы
        :param account: Кошелек для зачисления средств
        :param amount: Сумма платежа
        :param currency: Валюта платежа (по умолчанию RUB)
        :param payment_id: Номер заказа в вашем магазине (опционально)
        :return: Информация о выплате в формате:
        {
            "type": "success",
            "data": {
                "id": 185
            }
        }
        """
        params = {
            "i": payment_system_id,
            "account": account,
            "amount": amount,
            "currency": currency
        }
        
        if payment_id:
            params["paymentId"] = payment_id
            
        return self._make_api_request("withdrawals/create", params)

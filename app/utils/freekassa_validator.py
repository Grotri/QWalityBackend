import hashlib
import os
from typing import Dict, Any, Union, List

from app.utils.freekassa_exceptions import FreekassaWebhookError


class FreekassaValidator:
    """
    Класс для валидации уведомлений от FreeKassa
    """
    
    # IP адреса, с которых могут приходить уведомления от FreeKassa
    # Источник: https://docs.freekassa.ru/#section/1.-Vvedenie/1.4.-Opoveshenie-o-platezhe
    ALLOWED_IPS = [
        "168.119.157.136",
        "168.119.60.227",
        "138.201.88.124",
        "178.154.197.79",
        # Локальные IP для тестирования
        "127.0.0.1",
        "::1"
    ]
    
    @classmethod
    def validate_webhook(cls, 
                         data: Dict[str, Any], 
                         merchant_id: str = None, 
                         secret_key2: str = None,
                         client_ip: str = None) -> bool:
        """
        Валидирует webhook от FreeKassa
        :param data: Данные webhook
        :param merchant_id: ID магазина (если None, берется из переменных окружения)
        :param secret_key2: Секретный ключ 2 (если None, берется из переменных окружения)
        :param client_ip: IP адрес клиента (если None, проверка IP не производится)
        :return: True если webhook валиден, иначе вызывает исключение
        """
        # Проверка IP
        if client_ip and client_ip not in cls.ALLOWED_IPS:
            # Проверяем, не отключена ли проверка IP в тестовом режиме
            test_mode = os.getenv("FREEKASSA_TEST_MODE", "false").lower() == "true"
            if not test_mode:
                raise FreekassaWebhookError(f"Недопустимый IP адрес: {client_ip}")
        
        # Проверка наличия обязательных полей
        required_fields = ["MERCHANT_ID", "AMOUNT", "MERCHANT_ORDER_ID", "SIGN"]
        for field in required_fields:
            if field not in data:
                raise FreekassaWebhookError(f"Отсутствует обязательное поле: {field}")
        
        # Получаем merchant_id и secret_key2, если не переданы
        if not merchant_id:
            merchant_id = os.getenv("FREEKASSA_MERCHANT_ID")
        
        if not secret_key2:
            secret_key2 = os.getenv("FREEKASSA_SECRET_WORD2")
        
        # Проверка merchant_id
        if data["MERCHANT_ID"] != merchant_id:
            raise FreekassaWebhookError(f"Недопустимый MERCHANT_ID: {data['MERCHANT_ID']}")
        
        # Формируем и проверяем подпись
        sign_string = f"{data['MERCHANT_ID']}:{data['AMOUNT']}:{secret_key2}:{data['MERCHANT_ORDER_ID']}"
        expected_sign = hashlib.md5(sign_string.encode("utf-8")).hexdigest()
        
        if data["SIGN"].lower() != expected_sign.lower():
            raise FreekassaWebhookError("Недопустимая подпись")
        
        return True 
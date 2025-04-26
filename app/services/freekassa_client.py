import hashlib
import os
import urllib.parse


class FreeKassaClient:
    BASE_URL = "https://pay.freekassa.ru/"

    def __init__(self):
        self.merchant_id = os.getenv("FREEKASSA_MERCHANT_ID")
        self.secret_word = os.getenv("FREEKASSA_SECRET_WORD")  # Для формирования ссылки
        self.secret_word_2 = os.getenv("FREEKASSA_SECRET_WORD2")  # Для проверки webhook-а (если есть)

    def create_payment_url(self, amount: int, order_id: int, description: str, currency="RUB"):
        amount_rub = amount / 100  # У нас суммы в копейках

        params = {
            "m": self.merchant_id,
            "oa": f"{amount_rub:.2f}",
            "o": str(order_id),
            "currency": currency,
            "s": self._generate_signature(amount_rub, order_id)
        }

        url = f"{self.BASE_URL}?" + urllib.parse.urlencode(params)
        return url

    def _generate_signature(self, amount_rub, order_id):
        signature_string = f"{self.merchant_id}:{amount_rub:.2f}:{self.secret_word}:{order_id}"
        return hashlib.md5(signature_string.encode('utf-8')).hexdigest()

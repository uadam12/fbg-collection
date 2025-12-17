import requests
from django.conf import settings


class Paystack:
    BASE_URL = "https://api.paystack.co"

    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

    def init_payment(self, email, amount, callback_url, metadata: dict[str|int, str|int|bool]={}):
        """
        amount: int (Naira)
        """
        payload = {
            "email": email,
            "currency": "NGN",
            "amount": 100 * amount,
            "callback_url": callback_url,
        }

        if metadata: 
            payload['metadata'] = metadata

        response = requests.post(
            f"{self.BASE_URL}/transaction/initialize",
            headers=self.headers,
            json=payload,
            timeout=10,
        )

        return response.json()

    def verify_payment(self, reference):
        response = requests.get(
            f"{self.BASE_URL}/transaction/verify/{reference}",
            headers=self.headers,
            timeout=10,
        )

        return response.json()

paystack = Paystack()
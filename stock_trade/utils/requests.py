import requests
import json
from django.conf import settings
from rest_framework import status

from stock_trade.utils.custom_exceptions import StockQueryException


class PaystackPayment:
    """Paystack related request util."""

    def __init__(self, user=None):
        self.user = user
        self.secret = settings.PAYSTACK_AUTHORIZATION_SECRET
        self.headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.secret}'
        }
        self.base_url = settings.PAYSTACK_BASE_URL

    def initiate_paystack_transaction(self, amount_in_kobo, reference):
        url = f'{self.base_url}transaction/initialize'
        payload = {'reference': reference, 'amount': amount_in_kobo, 'email': self.user.email}
        return requests.post(url, data=json.dumps(payload), headers=self.headers)

    def verify_paystack_transaction(self, reference_id):
        url = f'{self.base_url}transaction/verify/{reference_id}'
        return requests.get(url, headers=self.headers)

    def charge_returning_customer(self, authorization_code, amount_in_kobo):
        url = f'{self.base_url}transaction/charge_authorization'
        payload = {
            'authorization_code': authorization_code,
            'email': self.user.email,
            'amount': amount_in_kobo
        }
        return requests.post(url, data=json.dumps(payload), headers=self.headers)


class IEXStockRequest:
    """IEX related request util."""

    def __init__(self):
        self.token = settings.IEX_SECRET_TOKEN
        self.base_url = settings.IEX_BASE_URL
        self.version = settings.IEX_VERSION
        self.headers = {'content-type': 'application/json'}

    def get_iex_stock_for_company(self, company_name):
        url = f'{self.base_url}{self.version}/stock/{company_name}/quote'
        response = requests.get(url, params={'token': self.token})

        if response.status_code != status.HTTP_200_OK:
            raise StockQueryException
        return json.loads(response.text)

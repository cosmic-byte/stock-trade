import requests
import json
from django.conf import settings

secret = settings.PAYSTACK_AUTHORIZATION_SECRET


class PaystackPayment:
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(secret)}

    def __init__(self, user=None):
        self.user = user

    def initiate_paystack_transaction(self, amount_in_kobo, reference):
        url = 'https://api.paystack.co/transaction/initialize'
        payload = {'reference': reference, 'amount': amount_in_kobo, 'email': self.user.email}
        return requests.post(url, data=json.dumps(payload), headers=self.headers)

    def verify_paystack_transaction(self, reference_id):
        url = 'https://api.paystack.co/transaction/verify/{}'.format(reference_id)
        return requests.get(url, headers=self.headers)

    def charge_returning_customer(self, authorization_code, amount_in_kobo):
        url = 'https://api.paystack.co/transaction/charge_authorization'
        payload = {'authorization_code': authorization_code, 'email': self.user.email, 'amount': amount_in_kobo}
        return requests.post(url, data=json.dumps(payload), headers=self.headers)

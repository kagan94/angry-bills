import requests
import json
from flask_login import current_user


class SebApi:
    API_URL = 'https://test.api.ob.baltics.sebgroup.com/v1'

    def __init__(self):
        ttp_token = """eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsdmY0MzJAbWFpbC5ydSIsImV4cCI6MTU1MDM5NDg0M30.PNC0Igse8izoiDhfqiHqEi3MQ_RXmsJO3rlHdlBrershU_WT1YRhVq8juaSygplQVspX59A6JduFJnW3skZmjw"""
        user_token = """eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJERU1PRUUsaWJzVXNlcjEiLCJleHAiOjE1NTAzOTQ3MTl9.uunOsh99Zp-lcOAkN6XpJ_q4h0JJ_XVaak3I-n_z6yXbw_bND1eb4kWm0WiF96Vnkr3NeEzC7DR62W3J3WgNFg"""

        self.ttp_token = ttp_token
        self.user_token = user_token

        self.headers = {
            'accept': "*/*",
            'content-type': "application/json",
            'Tpp-Token': ttp_token,
            'User-Token': user_token
        }

    def get_payments(self, size=10, date_from="2017-12-01", date_to="2018-03-01", page=0):
        endpoint = self.API_URL + '/bics/EEUHEE2X/accounts/eRnQSm4QiGMkHhr2UaStGizMjTr-BO9FkDkv8SuWc5E/transactions?'
        payload = {
            "from": date_from,
            "to": date_to,
            "page": page,
            "size": size
        }
        response = requests.get(endpoint, headers=self.headers, params=payload, verify=False)
        payment_info = response.json()["content"]
        return payment_info

    def create_payment(self, debtorAccount, creditorAccount, amount, endToEndPoint,
                             currency="EUR",creditor = "Test  user", debtor = "Debtor 1",
                             commentStructured="test refund", commentUnstructured = "test refund"):

        endpoint = self.API_URL + '/payments/sepa-credit-transfers/initiation/'

        payload = {
            "endToEndId": endToEndPoint,
            "debtorAccount": debtorAccount,
            "amount": amount,
            "currency": currency,
            "creditorAccount": creditorAccount,
            "remittanceInformationUnstructured": commentUnstructured,
            "remittanceInformationStructured": commentStructured,
            "creditor": creditor,
            "debtor": debtor
        }

        response = requests.post(endpoint, headers=self.headers, json=payload, verify=False)

        return response.status_code == 200

seb = SebApi()

endToEndId = "xxxxxxxxxxxxMxxxNxxxxxxxxxxxxxxx"
debtorAccount = "EE851010010530535012"
amount = "11"
currency = "EUR"
creditorAccount = "EE581010010607110014"

print(seb.get_payments())
print(seb.create_payment(debtorAccount, creditorAccount, amount, endToEndId))
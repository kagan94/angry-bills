import os

import requests
from flask_login import current_user


class SebApi:
    API_URL = 'https://test.api.ob.baltics.sebgroup.com/v1'

    def __init__(self):
        self.ttp_token = os.environ.get('SEB_TTP_TOKEN')
        self.user_token = current_user.seb_token

        self.headers = {
            'accept': "*/*",
            'content-type': "application/json",
            'Tpp-Token': self.ttp_token,
            'User-Token': self.user_token
        }

    def get_accounts(self):
        endpoint = self.API_URL + '/bics/EEUHEE2X/accounts'
        response = requests.get(endpoint, headers=self.headers, verify=False)
        payment_info = response.json()
        # Response example:
        # [{'accountId': 'sUv35WPgy2ZExCsqHko5kagTMqKbhxEqOUJwyWVsbiU', 'iban': 'EE651010010143685015',
        #                    'currency': 'EUR', 'accountType': 'CurrentAccount', 'alias': None, 'creditLimit': 0,
        #                    'reservedAmount': 0, 'balance': 989.0, 'availableBalance': 989.0,
        #                    'accountName': 'My EUR Business Account'}]
        return payment_info

    def find_iban(self, accounts, money_amount):
        for account in accounts:
            if account['balance'] >= money_amount:
                return account['iban']

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
                       currency="EUR", creditor="Test  user", debtor="Debtor 1",
                       commentStructured="test refund", commentUnstructured="test refund"):

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

# seb = SebApi()
#
# endToEndId = "xxxxxxxxxxxxMxxxNxxxxxxxxxxxxxxx"
# debtorAccount = "EE851010010530535012"
# amount = "11"
# currency = "EUR"
# creditorAccount = "EE581010010607110014"
#
# print(seb.get_payments())
# print(seb.create_payment(debtorAccount, creditorAccount, amount, endToEndId))

import requests
import json


class SebApi(object):

    def __init__(self, ttp_token, user_token):
        self.ttp_token = ttp_token
        self.user_token = user_token

        self.headers = {
            'accept': "application/json",
            'content-type': "*/*",
            'Tpp-Token': ttp_token,
            'User-Token': user_token
            }

    # def get_payments(self, start, end):
    #
    #     payload = {
    #         "from": start,
    #         "to": end,
    #
    #     }
    #
    #     request_url = """https://test.api.ob.baltics.sebgroup.com/v1/bics/EEUHEE2X/eris/payments?"""
    #
    #     r = requests.get(request_url, headers=self.headers, params=payload, verify=False)
    #     events = r.json()["events"]
    #     payment_ids = [event.get("paymentReferenceID") for event in events]
    #     return payment_ids
    #
    # def show_payments(self, payments_ids):
    #
    #     request_url = """https://test.api.ob.baltics.sebgroup.com/v1/payments/sepa-credit-transfers/initiation"""
    #
    #     payments_data = {}
    #
    #     for payment_id in payments_ids:
    #         payload = {
    #             "paymentId": payment_id
    #         }
    #
    #         r = requests.get(request_url, headers=self.headers, params=payload, verify=False)
    #         print(r.json())
    #         creation_time = r.json()["creationDateTime"]
    #         amount = r.json()["amount"]
    #         currency = r.json()["currency"]
    #         creditor = r.json()["creditor"]
    #         info = r.json()["remittanceInformationUnstructured"]
    #
    #         payments_data[payment_id] = [creation_time, amount, currency, creditor, info]
    #
    #     return payments_data

    def get_payments(self, n):
            payment_info = {}

            payload = {
                "from": "2017-12-01",
                "to": "2018-03-01",
                "page": 0,
                "size": n
            }

            request_url = """https://test.api.ob.baltics.sebgroup.com/v1/bics/EEUHEE2X/accounts/eRnQSm4QiGMkHhr2UaStGizMjTr-BO9FkDkv8SuWc5E/transactions?"""

            r = requests.get(request_url, headers=self.headers, params=payload, verify=False)

            for index, payment in enumerate(r.json()["content"]):
                amount = payment["transactionAmount"]
                currency = payment["transactionCurrency"]
                date = payment["bookdate"]
                party_name = payment["counterPartyName"]
                payment_info[index] = [amount, currency, date, party_name]

            return payment_info

TTP = """eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsdmY0MzJAbWFpbC5ydSIsImV4cCI6MTU1MDM5NDg0M30.PNC0Igse8izoiDhfqiHqEi3MQ_RXmsJO3rlHdlBrershU_WT1YRhVq8juaSygplQVspX59A6JduFJnW3skZmjw"""
USER = """eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJERU1PRUUsaWJzVXNlcjEiLCJleHAiOjE1NTAzOTQ3MTl9.uunOsh99Zp-lcOAkN6XpJ_q4h0JJ_XVaak3I-n_z6yXbw_bND1eb4kWm0WiF96Vnkr3NeEzC7DR62W3J3WgNFg"""

seb = SebApi(TTP, USER)
print(seb.get_payments(10))


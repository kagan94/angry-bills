import http.client

TTP = """eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsdmY0MzJAbWFpbC5ydSIsImV4cCI6MTU1MDM5NDg0M30.PNC0Igse8izoiDhfqiHqEi3MQ_RXmsJO3rlHdlBrershU_WT1YRhVq8juaSygplQVspX59A6JduFJnW3skZmjw"""
USER = """eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJERU1PRUUsaWJzVXNlcjEiLCJleHAiOjE1NTAzOTQ3MTl9.uunOsh99Zp-lcOAkN6XpJ_q4h0JJ_XVaak3I-n_z6yXbw_bND1eb4kWm0WiF96Vnkr3NeEzC7DR62W3J3WgNFg"""

conn = http.client.HTTPSConnection("test.api.ob.baltics.sebgroup.com")

headers = {
    'accept': "application/json",
    'content-type': "*/*",
    'tpp-token': TTP,
    'user-token': USER
    }

conn.request("GET", "/v1/bics/%7BEEUHEE2X%7D/accounts/%7BeRnQSm4QiGMkHhr2UaStGizMjTr-BO9FkDkv8SuWc5E%7D/transactions?from=2017-12-01&to=2018-03-01&page=0&size=50&type=SOME_STRING_VALUE", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
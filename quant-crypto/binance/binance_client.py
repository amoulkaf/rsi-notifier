import requests

class BinanceClient:
    def __init__(self, key):
        self.key = key

    def test_connectivity(self):
        r = requests.get('https://binance.com/api/v1/ping')
        return r.status_code

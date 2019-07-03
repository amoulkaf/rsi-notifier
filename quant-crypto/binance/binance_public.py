import requests
import json
import time
from .timeframe import Timeframe


class BinancePublicClient:
    klines = "/api/v1/klines"

    # Time conversion
    day = 86400 * 1000
    hour = 3600 * 1000
    minute = 60 * 1000

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def test_connectivity(self):
        r = requests.get('https://binance.com/api/v1/ping')
        return r.status_code

    def _get_records_api(self, ticker, interval, start_date, end_date):
        params = {
            "symbol": ticker,
            "interval": interval,
            "startTime": start_date,
            "endTime": end_date
        }

        r = requests.get("{}{}".format(self.endpoint, self.klines), params=params)
        return json.loads(r.text)

    def get_records(self, ticker, timeframe, interval, lookback):
        now = int(time.time()) * 1000

        if not isinstance(timeframe, Timeframe):
            raise TypeError('timeframe must be an instance of Timeframe Enum')

        return self._get_records_api(ticker='BTCUSDT', interval=('{}{}'.format(interval, timeframe.value[0])),
                                 start_date=(now - (timeframe.value[1] * lookback)),
                                 end_date=now)

    def get_opens(self, ticker, timeframe, interval, lookback):
        records = self.get_records(ticker, timeframe, interval, lookback)
        return list([record[1] for record in records])

    def get_highs(self, ticker, timeframe, interval, lookback):
        records = self.get_records(ticker, timeframe, interval, lookback)
        return list([record[2] for record in records])

    def get_lows(self, ticker, timeframe, interval, lookback):
        records = self.get_records(ticker, timeframe, interval, lookback)
        return list([record[3] for record in records])

    def get_closes(self, ticker, timeframe, interval, lookback):
        records = self.get_records(ticker, timeframe, interval, lookback)
        return list([record[4] for record in records])

    def get_volume(self, ticker, timeframe, interval, lookback):
        records = self.get_records(ticker, timeframe, interval, lookback)
        return list([record[5] for record in records])




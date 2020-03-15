import requests
import json
import time
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import datetime
import smtplib
from .timeframe import Timeframe


class BinancePublicClient:
    klines = "/api/v3/klines"

    # Time conversion
    day = 86400 * 1000
    hour = 3600 * 1000
    minute = 60 * 1000

    def __init__(self, endpoint):
        self.endpoint = endpoint

    @staticmethod
    def test_connectivity():
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

        return self._get_records_api(ticker=ticker, interval=('{}{}'.format(interval, timeframe.value[0])),
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

    def get_all_data(self, ticker, timeframe, interval, lookback):
        register_matplotlib_converters()
        records = self.get_records(ticker, timeframe, interval, lookback)
        start_date = datetime.datetime.fromtimestamp(int(float(records[0][0]) / 1000))
        end_date = datetime.datetime.fromtimestamp(int(float(records[len(records) - 1][0]) / 1000))
        if timeframe.value[0] == 'm':
            date_range = pd.date_range(start_date, end_date, freq='{}{}'.format(interval, 'min'))
        else:
            date_range = pd.date_range(start_date, end_date, freq='{}{}'.format(interval, timeframe.value[0]))
        date_range = date_range[-len(records):]
        for i in range(len(records)):
            records[i] = [float(x) for x in records[i][1:6]]
        df = pd.DataFrame.from_records(records, date_range, columns=["opens", "highs", "lows", "closes", "volume"])
        return df







import json
import pandas as pd
import pandas_ta as ta
import requests
import time
import numpy as np
from sklearn.linear_model import LinearRegression
from quant import linear_regression

_DAY_ = 86400 * 1000


def main():
    now = int(time.time()) * 1000
    params = {
        "symbol": "BTCUSDT",
        "interval": "1d",
        "startTime": now - _DAY_ * 15,
        "endTime": now
    }
    closes = list()
    r = requests.get('https://binance.com/api/v1/klines', params=params)
    records = json.loads(r.text)

    for record in records:
        closes.append(float(record[4]))

    rsi_lr = linear_regression.rsi_linear_regression(closes)
    print(rsi_lr)

if __name__ == '__main__':
    main()

import json
import pandas as pd
import pandas_ta as ta
import requests
import time
import numpy as np
from sklearn.linear_model import LinearRegression

_DAY_ = 86400 * 1000


def main():
    now = int(time.time()) * 1000
    params = {
        "symbol": "BTCUSDT",
        "interval": "4h",
        "startTime": now - _DAY_ * 15,
        "endTime": now
    }
    closes = list()
    r = requests.get('https://binance.com/api/v1/klines', params=params)
    records = json.loads(r.text)
    for record in records:
        closes.append(float(record[4]))

    closes_series = pd.Series(closes)
    rsi = ta.rsi(closes_series)

    rsi_array = pd.Series(rsi).values

    # TODO : First value is Nan ??
    rsi_array[0] = rsi_array[2]
    rsi_array[1] = rsi_array[2]

    prices = np.array(closes).reshape(-1, 1)

    model = LinearRegression().fit(prices, rsi_array)

    print("closes : %s" % closes)
    print("rsi : %s" % rsi_array)
    print("coefficient of determination : %s" % model.score(prices, rsi_array))
    print("intercept : %s" % model.intercept_)
    print("slope : %s" % model.coef_)


if __name__ == '__main__':
    main()

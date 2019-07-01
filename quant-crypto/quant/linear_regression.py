import pandas as pd
import pandas_ta as ta
import numpy as np
from sklearn.linear_model import LinearRegression


def rsi_linear_regression(closes):
    closes_series = pd.Series(closes)
    rsi = ta.rsi(closes_series)
    rsi_array = pd.Series(rsi).values
    # TODO : First value is Nan ??
    rsi_array[0] = rsi_array[2]
    rsi_array[1] = rsi_array[2]

    prices = np.array(closes).reshape(-1, 1)

    model = LinearRegression().fit(prices, rsi_array)

    results = {
        'coefficient of determination': model.score(prices, rsi_array),
        'intercept': model.intercept_,
        'slope': model.coef_,
    }
    return results

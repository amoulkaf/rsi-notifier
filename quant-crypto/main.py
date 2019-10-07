import datetime
import matplotlib.pyplot as plt
import pandas as pd
import pandas_ta as ta
import numpy
import scipy.signal
import seaborn as sb
import warnings


from binance.binance_public import BinancePublicClient
from binance.timeframe import Timeframe
from quant.graph import Graph


def main():
    client = BinancePublicClient('https://binance.com')
    dailyOnt = Graph(client, ticker='BTCUSDT', timeframe=Timeframe.DAY, interval=1, lookback=800, order = 4)
    dailyOnt.bearishRsi(plot=True)




if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()

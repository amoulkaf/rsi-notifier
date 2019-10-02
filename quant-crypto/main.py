import pandas as pd
import numpy
import datetime
import scipy.signal
import seaborn as sb
import matplotlib.pyplot as plt
from binance.binance_public import BinancePublicClient
from binance.timeframe import Timeframe


def main():
    client = BinancePublicClient('https://binance.com')
    df = client.get_all_data(ticker='BTCUSDT', timeframe=Timeframe.DAY, interval=1, lookback=200)
    closes = df['closes'].as_matrix()
    Lpeaks = scipy.signal.argrelmin(closes, order=3)
    df['Lpeaks'] = None
    for i in Lpeaks[0]:
        df['Lpeaks'].iloc[i] = df['closes'].iloc[i]
    fig, ax = plt.subplots()
    sb.lineplot(x=df.index, y='closes', data=df, ax=ax)
    sb.scatterplot(x=df.index, y='Lpeaks', data=df, ax=ax, color='r')
    plt.show()





if __name__ == '__main__':
    main()
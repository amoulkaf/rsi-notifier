import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import seaborn as sb
import pandas as pd
import pandas_ta as ta
import datetime

from binance.timeframe import Timeframe


class Graph:
    def __init__(self, client, ticker, timeframe, interval = 1, lookback=200, order = 3):
        self.df = client.get_all_data(ticker=ticker, timeframe=timeframe, interval=interval, lookback=lookback)
        self.order = order

    def bullishRsi(self, plot = False):
        df = self.df
        closes = df['closes'].as_matrix()
        lpeaks = scipy.signal.argrelmin(closes, order=self.order)
        df['Lpeaks'] = None
        for i in lpeaks[0]:
            df['Lpeaks'].iloc[i] = df['closes'].iloc[i]
        df['rsi'] = ta.rsi(df['closes'])
        ldf = df[(df['Lpeaks'].notnull())]
        ldf["rsidif"] = ldf["rsi"] - ldf["rsi"].shift(1)
        ldf["Lpeaksdif"] = ldf["Lpeaks"] - ldf["Lpeaks"].shift(1)
        ldf["Lrsidiv"] = ((ldf["rsidif"] > 0) & (ldf["Lpeaksdif"] < 0))
        df["Lrsidiv"] = ldf[ldf['Lrsidiv'] == True]['Lpeaks']
        if plot:
            self.indicatorPlot(df.index, df['closes'], df['rsi'], df['Lrsidiv'])
        return ldf["Lrsidiv"]

    def bearishRsi(self, plot = False):
        df = self.df
        closes = df['closes'].as_matrix()
        hpeaks = scipy.signal.argrelmax(closes, order=self.order)
        df['Hpeaks'] = None
        for i in hpeaks[0]:
            df['Hpeaks'].iloc[i] = df['closes'].iloc[i]
        df['rsi']=ta.rsi(df['closes'])
        hdf= df[(df['Hpeaks'].notnull())]
        hdf["rsidif"] = hdf["rsi"] - hdf["rsi"].shift(1)
        hdf["Hpeaksdif"] = hdf["Hpeaks"] - hdf["Hpeaks"].shift(1)
        hdf["Hrsidiv"] = ((hdf["rsidif"] < 0) & (hdf["Hpeaksdif"] > 0))
        df["Hrsidiv"] = hdf[hdf['Hrsidiv'] == True]['Hpeaks']
        if plot:
            self.indicatorPlot(df.index, df['closes'], df['rsi'], df['Hrsidiv'])
        return hdf["Hrsidiv"]

    @staticmethod
    def indicatorPlot(index, price, indicator, peaks=None):
        fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True,gridspec_kw={'width_ratios': [0.7]})
        ax1.plot(index, price)
        if peaks is not None:
            ax1.scatter(index, peaks)
        ax2.plot(index, indicator)
        ax1.get_shared_x_axes().join(ax1, ax2)
        plt.show()



import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import pandas as pd
import pandas_ta as ta


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

    def emascross(self, plot=False):
        df = self.df
        df['twentyema'] = ta.ema(df['closes'], 20)
        df['fiftyema'] = ta.ema(df['closes'], 50)
        # select 20 ema points where current 20 ema is below 50 ema , and previous 20 ema is above 50 ema
        df['bearishemaC'] = df[(df['twentyema'] < df['fiftyema']) & (df['twentyema'].shift(1) > df['fiftyema'].shift(1))]['twentyema']
        df['bullishemaC'] = df[(df['twentyema'] > df['fiftyema']) & (df['twentyema'].shift(1) < df['fiftyema'].shift(1))]['twentyema']
        if plot:
            plt.plot(df.index,df['closes'])
            plt.plot(df.index, df['twentyema'], color='green')
            plt.plot(df.index, df['fiftyema'], color='red')
            plt.scatter(df.index, df['bullishemaC'], color='yellow')
            plt.scatter(df.index, df['bearishemaC'], color='black')
            plt.show()

    def emapricecross(self, plot=False):
        df = self.df
        df['longema'] = ta.ema(df['closes'], 200)
        #select longema points where current ema is above close , and previous ema is below close
        df['bullishemaPC'] = df[(df['longema'] < df['closes']) & (df['longema'].shift(1) > df['closes'].shift(1))]['longema']
        df['bearishemaPC'] = df[(df['longema'] > df['closes']) & (df['longema'].shift(1) < df['closes'].shift(1))]['longema']
        if plot:
            plt.plot(df.index, df['closes'])
            plt.plot(df.index, df['longema'], color='black')
            plt.scatter(df.index, df['bullishemaPC'], color='yellow')
            plt.scatter(df.index, df['bearishemaPC'], color='red')
            plt.show()





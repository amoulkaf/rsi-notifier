import scipy.signal
import pandas as pd
import pandas_ta as ta


class RsiDivergence:
    def __init__(self, closes, order=3):
        self.df = pd.DataFrame(closes)
        self.order = order

    def bullish_rsi(self):
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
        return ldf["Lrsidiv"]

    def bearish_rsi(self):
        df = self.df
        closes = df['closes'].as_matrix()
        hpeaks = scipy.signal.argrelmax(closes, order=self.order)
        df['Hpeaks'] = None
        for i in hpeaks[0]:
            df['Hpeaks'].iloc[i] = df['closes'].iloc[i]
        df['rsi'] = ta.rsi(df['closes'])
        hdf = df[(df['Hpeaks'].notnull())]
        hdf["rsidif"] = hdf["rsi"] - hdf["rsi"].shift(1)
        hdf["Hpeaksdif"] = hdf["Hpeaks"] - hdf["Hpeaks"].shift(1)
        hdf["Hrsidiv"] = ((hdf["rsidif"] < 0) & (hdf["Hpeaksdif"] > 0))
        return hdf["Hrsidiv"]

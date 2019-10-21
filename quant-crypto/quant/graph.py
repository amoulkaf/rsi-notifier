import scipy.signal
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class IndicatorAnalysis:
    def __init__(self, client, ticker, timeframe, interval=1, lookback=200, order=3, fromcsv=False):
        if fromcsv:
            self.df = pd.read_csv("./data/btc.csv")
        else:
            self.df = client.get_all_data(ticker=ticker, timeframe=timeframe, interval=interval, lookback=lookback)
            self.order = order
        self.ichimoku = None
        self.spandf = None
        closes = df['closes'].as_matrix()
        lpeaks = scipy.signal.argrelmin(closes, order=self.order)
        self.df['Lpeaks'] = None
        for i in lpeaks[0]:
            self.df['Lpeaks'].iloc[i] = self.df['closes'].iloc[i]
        hpeaks = scipy.signal.argrelmax(closes, order=self.order)
        self.df['Hpeaks'] = None
        for i in hpeaks[0]:
            self.df['Hpeaks'].iloc[i] = self.df['closes'].iloc[i]

    def heiken_ashi(self):
        df = self.df
        df['HA_Close'] = (df['closes'] + df['opens'] + df['highs'] + df['lows']) / 4
        idx = df.index.name
        df.reset_index(inplace=True)
        ha_open = [(df['opens'][0] + df['closes'][0]) / 2]
        [ha_open.append((ha_open[i] + df['HA_Close'].values[i]) / 2) \
         for i in range(0, len(df) - 1)]
        df['HA_Open'] = ha_open
        df.set_index('index', inplace=True)
        df['HA_High'] = df[['HA_Open', 'HA_Close', 'highs']].max(axis=1)
        df['HA_Low'] = df[['HA_Open', 'HA_Close', 'lows']].min(axis=1)

    def bullish_rsi(self):
        df = self.df
        df['rsi'] = ta.rsi(df['closes'])
        ldf = df[(df['Lpeaks'].notnull())]
        ldf["rsidif"] = ldf["rsi"] - ldf["rsi"].shift(1)
        ldf["Lpeaksdif"] = ldf["Lpeaks"] - ldf["Lpeaks"].shift(1)
        ldf["Lrsidiv"] = ((ldf["rsidif"] > 0) & (ldf["Lpeaksdif"] < 0))
        df["Lrsidiv"] = ldf[ldf['Lrsidiv'] == True]['Lpeaks']
        return ldf["Lrsidiv"]

    def bearish_rsi(self):
        df = self.df
        df['rsi'] = ta.rsi(df['closes'])
        hdf = df[(df['Hpeaks'].notnull())]
        hdf["rsidif"] = hdf["rsi"] - hdf["rsi"].shift(1)
        hdf["Hpeaksdif"] = hdf["Hpeaks"] - hdf["Hpeaks"].shift(1)
        hdf["Hrsidiv"] = ((hdf["rsidif"] < 0) & (hdf["Hpeaksdif"] > 0))
        df["Hrsidiv"] = hdf[hdf['Hrsidiv'] == True]['Hpeaks']
        return hdf["Hrsidiv"]

    def emas_cross(self):
        df = self.df
        df['twentyema'] = ta.ema(df['closes'], 20)
        df['fiftyema'] = ta.ema(df['closes'], 50)
        # select 20 ema points where current 20 ema is below 50 ema , and previous 20 ema is above 50 ema
        df['bearishemaC'] = \
        df[(df['twentyema'] < df['fiftyema']) & (df['twentyema'].shift(1) > df['fiftyema'].shift(1))]['twentyema']
        df['bullishemaC'] = \
        df[(df['twentyema'] > df['fiftyema']) & (df['twentyema'].shift(1) < df['fiftyema'].shift(1))]['twentyema']

    def ema_price_cross(self):
        df = self.df
        df['longema'] = ta.ema(df['closes'], 200)
        # select longema points where current ema is above close , and previous ema is below close
        df['bullishemaPC'] = df[(df['longema'] < df['closes']) & (df['longema'].shift(1) > df['closes'].shift(1))][
            'longema']
        df['bearishemaPC'] = df[(df['longema'] > df['closes']) & (df['longema'].shift(1) < df['closes'].shift(1))][
            'longema']

    def ichimoku_cloud(self,p1,p2,p3,p4):
        self.ichimoku, self.spandf = ta.ichimoku(self.df['highs'], self.df['lows'], self.df['closes'], p1, p2, p3, p4)
        self.spandf = self.spandf.shift(-31, freq='D')
        print(self.ichimoku.tail())
        print(self.spandf.head())

    def plot_chart(self, ha=False, emapc=False, emac=False, rsi=False):
        df = self.df
        fig = make_subplots(rows=2, cols=1,
                            shared_xaxes=True)
        if ha:
            if not ('HA_Close' in df):
                self.heiken_ashi()
            main = go.Figure(data=[go.Candlestick(x=df.index,
                                                  open=df['HA_Open'],
                                                  high=df['HA_High'],
                                                  low=df['HA_Low'],
                                                  close=df['HA_Close'])])
        else:
            main = go.Candlestick(x=df.index,
                                  open=df['opens'],
                                  high=df['highs'],
                                  low=df['lows'],
                                  close=df['closes'])
        fig.append_trace(main, 1, 1)
        if emapc:
            if not ('bullishemaPC' in df):
                self.ema_price_cross()
            fig.add_trace(go.Scatter(x=df.index, y=df['longema'],
                                     mode='lines',
                                     line_color='red',
                                     name='longema'))
            fig.add_trace(go.Scatter(x=df.index, y=df['bullishemaPC'],
                                     mode='markers',
                                     marker_size=10,
                                     marker_color='rgba(255, 182, 193, .9)',
                                     name='bullishemaPC'))
            fig.add_trace(go.Scatter(x=df.index, y=df['bearishemaPC'],
                                     mode='markers',
                                     marker_size=10,
                                     marker_color='rgba(152, 0, 0, .8)',
                                     name='bearishemaPC'))

        if emac:
            if not ('twentyema' in df):
                self.emas_cross()
            fig.add_trace(go.Scatter(x=df.index, y=df['twentyema'],
                                     mode='lines',
                                     line_color='blue',
                                     name='twentyema'))
            fig.add_trace(go.Scatter(x=df.index, y=df['fiftyema'],
                                     mode='lines',
                                     line_color='orange',
                                     name='fiftyema'))
            fig.add_trace(go.Scatter(x=df.index, y=df['bearishemaC'],
                                     mode='markers',
                                     marker_size=5,
                                     marker_color='rgba(152, 0, 0, .8)',
                                     name='bearishemaC'))
            fig.add_trace(go.Scatter(x=df.index, y=df['bullishemaC'],
                                     mode='markers',
                                     marker_size=5,
                                     marker_color='rgba(255, 182, 193, .9)',
                                     name='bullishemaC'))
        fig.add_trace(go.Scatter(x=self.ichimoku.index, y=self.ichimoku['ISA_20'],
                                 mode='lines',
                                 line_color='green',
                                 name='ISA_20'))
        fig.add_trace(go.Scatter(x=self.ichimoku.index, y=self.ichimoku['ISB_60'],
                                 mode='lines',
                                 fill='tonexty',
                                 line_color='red',
                                 name='ISB_60'))
        fig.add_trace(go.Scatter(x=self.spandf.index, y=self.spandf['ISA_20'],
                                 mode='lines',
                                 line_color='green',
                                 name='ISA_20'))
        fig.add_trace(go.Scatter(x=self.spandf.index, y=self.spandf['ISB_60'],
                                 mode='lines',
                                 fill='tonexty',
                                 line_color='red',
                                 name='ISB_60'))
        fig.add_trace(go.Scatter(x=self.ichimoku.index, y=self.ichimoku['ITS_20'],
                                 mode='lines',
                                 name='ITS_20'))
        fig.add_trace(go.Scatter(x=self.ichimoku.index, y=self.ichimoku['IKS_60'],
                                 mode='lines',
                                 name='IKS_60'))
        fig.add_trace(go.Scatter(x=self.ichimoku.index, y=self.ichimoku['ICS_60'],
                                 mode='lines',
                                 name='ICS_60'))
        # main chart end
        if rsi:
            if not ('Lrsidiv' in df or 'Hrsidiv' in df):
                self.bearish_rsi()
                self.bullish_rsi()
            rsip = go.Scatter(
                x=df.index,
                y=df['rsi'],
                name='rsi'
            )
            fig.add_trace(go.Scatter(x=df.index, y=df['Lrsidiv'],
                                     mode='markers',
                                     marker_size=15,
                                     marker_color='rgba(11, 156, 49, .9)',
                                     name='bullish Rsi'))
            fig.add_trace(go.Scatter(x=df.index, y=df['Hrsidiv'],
                                     mode='markers',
                                     marker_size=15,
                                     marker_color='rgba(255, 20, 20, .9)',
                                     name='bearish Rsi'))
            fig.append_trace(rsip, 2, 1)
            fig['layout']['yaxis1'].update(domain=[0, 0.7])
            fig['layout']['yaxis2'].update(domain=[0.7, 1])
        else:
            fig['layout']['yaxis1'].update(domain=[0, 1])

        fig.write_html('first_figure.html', auto_open=True)

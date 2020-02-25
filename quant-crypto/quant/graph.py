import scipy.signal
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib.abstract as tal
import plotly.graph_objects as go
import smtplib
from .notification import notification
from plotly.subplots import make_subplots
import logging
import boto3
import json

with open('./quant/config.json') as json_file:
    data = json.load(json_file)
    BUCKET_NAME = data['s3']['bucket_name']
    BUCKET_REGION = data['s3']['bucket_region']


class IndicatorAnalysis:
    def __init__(self, client, ticker, timeframe, interval=1, lookback=200, order=3, fromcsv=False):
        if fromcsv:
            self.df = pd.read_csv("./data/{}.csv".format(ticker))
        else:
            self.df = client.get_all_data(ticker=ticker, timeframe=timeframe, interval=interval, lookback=lookback*interval)
        self.order = order
        self.ticker = ticker
        self.timeframe = timeframe
        self.interval = interval
        self.lpeaks = scipy.signal.argrelmin(self.df['closes'].values, order=self.order)
        self.hpeaks = scipy.signal.argrelmax(self.df['closes'].values, order=self.order)


        self.rsi_divergence()

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

    def rsi_divergence(self):
        df = self.df
        df['close'] = df['closes']
        df['rsi'] = tal.RSI(df)

        df['Lpeaksdif'] = df.iloc[self.lpeaks[0]]['close'] - df.iloc[self.lpeaks[0]]['close'].shift(1)
        df['Lrsidif'] = df.iloc[self.lpeaks[0]]['rsi'] - df.iloc[self.lpeaks[0]]['rsi'].shift(1)
        df['Lrsidiv'] = (df['Lrsidif'] > 0) & (df['Lpeaksdif'] < 0)
        df['Lrsidiv'] = df[df['Lrsidiv']==True]['close']
        #
        df['Hpeaksdif'] = df.iloc[self.hpeaks[0]]['close'] - df.iloc[self.hpeaks[0]]['close'].shift(1)
        df['Hrsidif'] = df.iloc[self.hpeaks[0]]['rsi'] - df.iloc[self.hpeaks[0]]['rsi'].shift(1)
        df['Hrsidiv'] = (df['Hrsidif'] > 0) & (df['Hpeaksdif'] < 0)
        df['Hrsidiv'] = df[(df['Hrsidif'] < 0) & (df['Hpeaksdif'] > 0)]['close']


        if not np.isnan(df["Lrsidiv"].iloc[1-self.order]):
            notification("bullish rsi divergence", self.ticker, self.interval, self.timeframe, self.plot_chart())
        if not np.isnan(df["Hrsidiv"].iloc[1 - self.order]):
            notification("bearish rsi divergence", self.ticker, self.interval, self.timeframe, self.plot_chart())

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


    def plot_chart(self, ha=False, emapc=False, emac=False, rsi=True):
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

        # main chart end
        if rsi:

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
        filename = self.ticker+self.timeframe.name + str(self.interval) + '.html'
        fig.write_html(filename, auto_open=True)
        s3 = boto3.client('s3')
        s3.upload_file(filename, BUCKET_NAME, filename ,ExtraArgs={'ContentType': 'text/html'})
        return "https://" + BUCKET_NAME+".s3."+BUCKET_REGION+".amazonaws.com/" + filename

import scipy.signal
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class PatternsAnalysis:
    def __init__(self, client, ticker, timeframe, interval=1, lookback=200, order=3, from_csv=False):
        if from_csv:
            self.df = pd.read_csv("./data/btc.csv")
        else:
            self.df = client.get_all_data(ticker=ticker, timeframe=timeframe, interval=interval, lookback=lookback)
            self.order = order
        closes = self.df['closes'].as_matrix()
        lpeaks = scipy.signal.argrelmin(closes, order=self.order)
        self.df['Lpeaks'] = None
        for i in lpeaks[0]:
            self.df['Lpeaks'].iloc[i] = self.df['closes'].iloc[i]
        hpeaks = scipy.signal.argrelmax(closes, order=self.order)
        self.df['Hpeaks'] = None
        for i in hpeaks[0]:
            self.df['Hpeaks'].iloc[i] = self.df['closes'].iloc[i]

    def support_resistance(self):
        df=self.df
        df['supportLine'] = None
        df.reset_index(inplace=True)
        lines = []
        i=0
        lows_line = []
        for index, row in df.iterrows():
            if row['Lpeaks']:
                lows_line.append((index,row['Lpeaks'],row['index']))
                if len(lows_line)>3:
                    lows_line.pop(0)
                if len(lows_line)>2:
                    area = lows_line[0][0] * (lows_line[1][1] - lows_line[2][1]) + \
                           lows_line[2][0] * (lows_line[2][1] - lows_line[0][1]) + \
                           lows_line[2][0] * (lows_line[0][1] - lows_line[1][1])
                    area = area / (2* row['Lpeaks'])
                    if area < 10:
                        if i > 0 and lows_line[1] in lines[i-1]:
                            lines[i-1].append(lows_line[2])
                        else:
                            lines.append(lows_line)
                            lows_line = []
                            i+=1

        df.set_index('index', inplace=True)
        for x in lines:
            for _, price, ind in x:
                df.loc[ind,'supportLine'] = price

        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df['opens'],
                                             high=df['highs'],
                                             low=df['lows'],
                                             close=df['closes'])])
        fig.add_trace(go.Scatter(x=df.index, y=df['Lpeaks'],
                                 mode='markers',
                                 marker_size=15,
                                 marker_color='rgba(11, 156, 49, .9)',
                                 name='ISA_20'))
        fig.write_html('first_figure.html', auto_open=True)




import warnings

from binance.binance_public import BinancePublicClient
from binance.timeframe import Timeframe
from quant.graph import Graph


def main():
    client = BinancePublicClient('https://binance.com')
    dailyBtc = Graph(client, ticker='BTCUSDT', timeframe=Timeframe.DAY, interval=1, lookback=400, order=4)
    dailyBtc.plot_chart(False, True, True, True)


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()

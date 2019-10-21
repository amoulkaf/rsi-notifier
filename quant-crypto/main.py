import warnings

from binance.binance_public import BinancePublicClient
from binance.timeframe import Timeframe
from quant.graph import IndicatorAnalysis
from quant.patterns import PatternsAnalysis


def main():
    client = BinancePublicClient('https://binance.com')
    daily_btc = PatternsAnalysis(client, ticker='BTCUSDT', timeframe=Timeframe.DAY, interval=1, lookback=400, order=4)
    daily_btc.support_resistance()

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()

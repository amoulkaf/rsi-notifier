import pandas as pd
import datetime
import scipy
from binance.binance_public import BinancePublicClient
from binance.timeframe import Timeframe




def main():
    client = BinancePublicClient('https://binance.com')
    df = client.get_all_data(ticker='BTCUSDT', timeframe=Timeframe.DAY, interval=1, lookback=200)
    closes = df['closes'].as_matrix()
    print(type(closes))





if __name__ == '__main__':
    main()
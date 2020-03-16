import warnings
import threading
import time
from binance.binance_public import BinancePublicClient
from binance.timeframe import Timeframe
from quant.graph import IndicatorAnalysis
from datetime import datetime



def main(timeframe, interval, order):
    print("started")
    client = BinancePublicClient('https://binance.com')
    if timeframe.value[0] == 'm':
        tickers = ['BTCUSDT']
    else:
        tickers = ['BTCUSDT', 'BNBUSDT', 'ETHUSDT', 'XRPUSDT', 'LTCUSDT', 'BCHUSDT', 'ADAUSDT', 'NEOUSDT']
    while True:
        for ticker in tickers:
            IndicatorAnalysis(client, ticker=ticker, timeframe=timeframe, interval=interval, lookback=80,
                                      order=order, aws=False)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time +": finished "+ timeframe.name + str(interval))
        time.sleep(timeframe.value[1] * interval/1000)


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        threads = []
        threads.append(threading.Thread(target=main, args=(Timeframe.DAY, 1, 3)))
        threads.append(threading.Thread(target=main, args=(Timeframe.MINUTE, 15, 4)))
        threads.append(threading.Thread(target=main, args=(Timeframe.MINUTE, 5, 4)))
        threads.append(threading.Thread(target=main, args=(Timeframe.HOUR, 4, 3)))
        for t in threads:
           t.start()


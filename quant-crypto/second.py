from datetime import datetime
import json
import time
from main import get_records
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import pandas as pd
import pandas_ta as ta


def machart(df, kind, fast, medium, slow, append=True, last=400, figsize=(16, 8)):
    ma1 = df.ta(kind=kind, length=fast, append=append)
    ma2 = df.ta(kind=kind, length=medium, append=append)
    ma3 = df.ta(kind=kind, length=slow, append=append)
    pricedf = df[['close', ma1.name, ma2.name, ma3.name]]
    title = f"{df.name}: 1H {kind.upper()}s from {df.index[0]} to {df.index[-1]} ({last})"
    pricedf = df[['close', ma1.name, ma2.name, ma3.name]]
    pricedf.tail(last).plot(figsize=figsize, color=['black', 'green', 'orange', 'red'], title=title, grid=True)


def main():
    records = get_records("BTCUSDT", "1h")
    closes = []
    opens = []
    volume = []
    highs = []
    lows = []
    start_date = datetime.fromtimestamp(int(float(records[0][0]) / 1000))
    end_date = datetime.fromtimestamp(int(float(records[len(records) - 1][0]) / 1000))
    index = pd.date_range(start_date, end_date, freq='1H')
    for record in records:
        opens.append(int(float(record[1])))
        highs.append(int(float(record[2])))
        lows.append(int(float(record[3])))
        closes.append(int(float(record[4])))
        volume.append(int(float(record[5])))
    df = pd.DataFrame({
        'index': index,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volume
    },
        index=index)
    print(index)
    df.set_index('index')
    df.name = 'BTCUSDT'
    df.ta.constants(True, -4, 4)
    df.tail()
    machart(df, 'ema', 50, 100, 200)
    plt.show()


if __name__ == '__main__':
    main()

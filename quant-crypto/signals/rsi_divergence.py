import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import datetime


def nice_angle(a, b, c):
    # expect a, b ,c to be price at 3 consecutive times
    a = np.array([0, a])
    b = np.array([1, b])
    c = np.array([2, c])
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    print(a)
    print(np.degrees(angle))
    return True


class RsiDivergence:

    def get_successive_highs(self, peaks, position, minimum_range):
        highs = []
        for i in range(minimum_range + position, len(peaks)):
            if not pd.isnull(peaks[i]) and peaks[i] > peaks[position]:
                highs.append(i)
        return highs

    def does_segments_cross(self, p1, p2, p3, p4):
        pass

    def higher_highs(self, peaks):
        a = peaks
        peaks_list = list()  # [v for i, v in peaks.item() if (not pd.isnull(v))]
        higher_highs = list()
        #
        # for i, v in peaks.items():
        #     if not pd.isnull(v):
        #         peaks_list.append(v)

        for i, v in enumerate(peaks_list):
            successive_highs = self.get_successive_highs(peaks, i, 4)

    @staticmethod
    def nice_peak(df):
        # tries to select only peaks that have a minimum of variation compared to they right and left points
        # calculates the sum of the rise before the peak(%) , and the drop after it , and returns true if it is higher than a minimum
        # a naive way to write it is 2 * df.data - df.data.shift(1) - df.data.shift(-1)) / df.data.mean() > 0.02
        print("shit is ")
        print((2 * df.data - df.data.shift(1) - df.data.shift(-1)) / df.data.mean())
        print("real")
        return True

    def peaks(self, data):
        # Generate a noisy AR(1) sample
        start_date = datetime.datetime.fromtimestamp(int(float(data[0][0]) / 1000))
        end_date = datetime.datetime.fromtimestamp(int(float(data[len(data) - 1][0]) / 1000))
        date_range = pd.date_range(start_date, end_date, freq='1D')

        closes = []
        opens = []
        volume = []
        highs = []
        lows = []

        for record in data:
            opens.append(int(float(record[1])))
            highs.append(int(float(record[2])))
            lows.append(int(float(record[3])))
            closes.append(int(float(record[4])))
            volume.append(int(float(record[5])))

        df = pd.DataFrame({
            'close': closes,
            'date': date_range
        })

        # Find local peaks
        # df['min'] = df.data[(df.data.shift(1) > df.data) & (df.data.shift(-1) > df.data)]
        df['max'] = df.close[(df.close.shift(1) < df.close) & (df.close.shift(-1) < df.close)]
        for i in range(0, df.size):
        df['highs'] = df[df.max > 1000]

        # self.higher_highs(df['max'])
        # Plot results
        # plt.scatter(df.index, df['min'], c='r')
        # df.plot.scatter(df.index, df['max'], c='g')
        print(df.head)
        # df.Time = df.Time.dt.time
        # df.plot.scatter(df['max'])
        df.set_index('date', inplace=True)
        df.plot.line()
        plt.show()

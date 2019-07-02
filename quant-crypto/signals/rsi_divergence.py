import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class RsiDivergence():

    def peaks(self, data):
        # Generate a noisy AR(1) sample
        np.random.seed(0)

        rs = data
        xs = []
        for r in rs:
            xs.append(float(r))

        df = pd.DataFrame(xs, columns=['data'])

        # Find local peaks
        # df['min'] = df.data[(df.data.shift(1) > df.data) & (df.data.shift(-1) > df.data)]
        df['max'] = df.data[(df.data.shift(1) < df.data) & (df.data.shift(-1) < df.data)]

        # Plot results
        # plt.scatter(df.index, df['min'], c='r')
        plt.scatter(df.index, df['max'], c='g')
        df.data.plot()
        plt.show()
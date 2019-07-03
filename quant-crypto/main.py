from binance.binanxce_public import BinancePublicClient
from binance.timeframe import Timeframe

from signals.rsi_divergence import RsiDivergence

# _DAY_ = 86400 * 1000
#
# def newline(p1, p2):
#     ax = plt.gca()
#     xmin, xmax = ax.get_xbound()
#
#     if(p2[0] == p1[0]):
#         xmin = xmax = p1[0]
#         ymin, ymax = ax.get_ybound()
#     else:
#         ymax = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmax-p1[0])
#         ymin = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmin-p1[0])
#
#     l = mlines.Line2D([xmin,xmax], [ymin,ymax], color="Red")
#     ax.add_line(l)
#     return l
#
#
# def main():
#     closes = list()
#     records = get_records("BTCUSDT", "1h")
#     for record in records:
#         closes.append(int(float(record[4])))
#     print("closes : %s" % closes)
#     # x = electrocardiogram(closes)
#     peaks, _ = find_peaks(closes, height=0)
#     plt.plot(closes)
#
#     # plt.plot(peaks, closes[peaks], "x")
#     plt.plot(np.zeros_like(closes), "--", color="gray")
#     p1 = [peaks[0], closes[peaks[0]]]
#     p2 = [peaks[1], closes[peaks[1]]]
#     newline(p1, p2)
#     plt.show()
#
#     print("peaks : %s" % peaks)
#
#     rsi_lr = linear_regression.rsi_linear_regression(closes)
#     print(rsi_lr)

def main():
    client = BinancePublicClient('https://binance.com')
    response = client.get_closes(ticker='BTCUSDT', timeframe=Timeframe.HOUR, interval=1, lookback=200)
    rsi_divergence = RsiDivergence()
    rsi_divergence.peaks(response)


if __name__ == '__main__':
    main()




import pandas as pd
import pandas_ta as ta

def main():
    df = pd.read_csv('data/spy.csv', sep=',')
    df.ta.log_return(cumulative=True, append=True)
    df.ta.percent_return(cumulative=True, append=True)
    df.columns
    df.tail()

if __name__ == '__main__':
    main()


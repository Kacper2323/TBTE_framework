import matplotlib.pyplot as plt
import matplotlib.colors
import pandas as pd

'''
Set of utility functions for plotting/manipulating time based data.
'''

__all__ = ['check_completeness', 'ms_to_time', 'time_to_ms', 'kline_quickchart']

def check_completeness(data: pd.DataFrame,
                       freq: str, 
                       index: bool=True, 
                       time_feature: str=None, 
                       show_plot :bool=False
                       ) -> list:

    '''
    Check temporal data for completeness. Accepts data sorted by time with DateTime feature.

    parameters
    ----------
    data: Pandas dataframe
    index: bool 
        If time data is in the index
    time_feature: str
        if *index* is false, column with time data
    freq: str 
        pandas freq ex. '15min'
    show_plot: bool
        show plot of missing values

    returns
    -------
    missing_data: list of tuples
        contains list of tuples with intervals of missing data eg. [(15:30, 16:45), (19:00, 23:00)]
    '''

    if index:
        time_range = pd.date_range(data.index.min(), data.index.max(), freq=freq)
        diff = pd.Series(time_range.difference(data.index))
    else:
        time_range = pd.date_range(data[time_feature].min(), data[time_feature].max(), freq=freq)
        diff = pd.Series(time_range.difference(data[time_feature]))
        
    if diff.empty:
        return []
        
    missing_data = []   #this is the return value, code below calculates ranges based on list of missing timestamps
    beg = diff[0]
    for i in diff.index:
        if i == diff.index.max():
            missing_data.append((beg, diff[i]))
            break
        if diff[i] + time_range.freq == diff[i+1]:
            continue
        else:
            missing_data.append((beg, diff[i]))
            beg = diff[i+1]
    
    if show_plot == True:

        time_x = pd.DataFrame(time_range)
        time_x.set_index(0, inplace=True)

        plt.figure(figsize=(20,5))

        x_plot = list(range(0, len(time_range)))
        y_plot = [1 if i in data.index else 0 for i in time_range]

        plt.scatter(x=x_plot, y=y_plot, marker=".", c=y_plot, cmap = matplotlib.colors.ListedColormap(['red', 'green']))

        plt.yticks([0, 1], ["missing", "present"])
        plt.ylim(-1, 2)

        x_labels = [item for t in missing_data for item in t]
        x_ticks = [len(time_x.loc[:i, :])-1 for i in x_labels]

        plt.xticks( x_ticks , x_labels)
        plt.xticks(rotation=35, ha='right')

        plt.grid(visible=True, which='both', axis='x', color='grey', linewidth=1)
        plt.rcParams['axes.facecolor'] = '0.9'
        plt.title("Missing data time chart")
        plt.show()

    return missing_data


def ms_to_time(feature: pd.Series) -> pd.Series:
    return pd.to_datetime(feature, unit='ms')


def time_to_ms(feature: pd.Series) -> pd.Series:
    return feature.astype('int64').astype('float') / 10**6


def kline_quickchart(data: pd.DataFrame, interval: int) -> None:

    '''
    Create a quick, non-interactive klines chart.

    parameters
    ----------
    data: pandas DataFrame
        klines data containing ["Open", "Close", "Low", "High"] features
    interval: int
        number of rows/klines to be displayed

    returns
    -------
    None
    '''
    plt.figure(figsize=(20,10))

    kline_width = 0.8
    candle_width = 0.2

    prices = data.tail(interval)
    prices.index = pd.to_datetime(prices.index, unit='ms')

    prices_up = prices.loc[prices.Open<=prices.Close, :]
    prices_down = prices.loc[prices.Open>prices.Close, :]

    x_labels_up = list(prices_up.index)
    x_labels_down = list(prices_down.index)

    x_ticks_up = [len(prices.loc[:i, :])-1 for i in x_labels_up]
    x_ticks_down = [len(prices.loc[:i, :])-1 for i in x_labels_down]

    up_color = 'green'
    down_color = 'red'
    plt.xticks(rotation=45, ha='right')

    plt.bar(x_ticks_up, prices_up.Close - prices_up.Open, width=kline_width, bottom=prices_up["Open"], color=up_color)
    plt.bar(x_ticks_up, prices_up.Low - prices_up.Open, width=candle_width, bottom=prices_up["Open"], color=up_color)
    plt.bar(x_ticks_up, prices_up.High - prices_up.Close, width=candle_width, bottom=prices_up["Close"], color=up_color)

    plt.bar(x_ticks_down, prices_down.Close - prices_down.Open, width=kline_width, bottom=prices_down["Open"], color=down_color)
    plt.bar(x_ticks_down, prices_down.Low - prices_down.Close, width=candle_width, bottom=prices_down["Close"], color=down_color)
    plt.bar(x_ticks_down, prices_down.High - prices_down.Open, width=candle_width, bottom=prices_down["Open"], color=down_color)

    if interval>25:
        custom_ticks = range(interval-1, 0, -int(interval/25))
        custom_labels = prices.iloc[custom_ticks].index
        plt.xticks(custom_ticks, custom_labels)
    else:
        plt.xticks(range(0, interval), prices.index)

    plt.grid(visible=True, which='major', axis='both', color='gray', linewidth=0.2)
    plt.title('BTC - BUSD')
    plt.show()
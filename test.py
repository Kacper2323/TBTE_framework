from PROJECT_MODULE.BinanceAPI import BinanceAPI as BA
from PROJECT_MODULE.TemporalDataUtils import *


url = 'https://data-api.binance.vision'
api_calls = {'time': '/api/v3/time',
             'klines': '/api/v3/klines'}

data = BA.get_recent_klines('BTCBUSD', interval='15m', output='dataframe')

kline_quickchart(data=data, interval=100)


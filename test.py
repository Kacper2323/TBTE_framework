from PROJECT_MODULE.ApiWrapper import CallWrapper
from PROJECT_MODULE.TemporalDataUtils import *


url = 'https://data-api.binance.vision'
api_calls = {'time': '/api/v3/time',
             'klines': '/api/v3/klines'}

api = CallWrapper(url=url, apiCalls=api_calls)

data = api.get_recent_klines(symbol='BTCBUSD', interval='1d')

kline_quickchart(data=data, interval=100)
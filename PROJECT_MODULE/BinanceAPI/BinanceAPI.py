import requests
import json
import pandas as pd
from PROJECT_MODULE.BinanceAPI.BinanceVars import *

def _status(api_response: requests.Response) -> int:
    
    value = api_response.status_code
    match value:
        case 404:
            print("Resource not found ({})".format(value))
            return 0
        case 429 | 418 | 403:
            print("Too many requests {}".format(value))
            return 0
        case 200:
            return 1
        case _:
            print("Unknown exit status code: {}".format(value))
            return 0


def get_server_time() -> requests.Response:

    if 'time' not in binance_api_endpoints:
        print("No 'time' API endpoint on record.")
        return -1
    
    response = requests.get(binance_url + binance_api_endpoints['time'])

    if not _status(response):
        return -1
    return response


def get_recent_klines(symbol: str, interval: str, output='dataframe') -> pd.DataFrame:
    '''
    sends a GET request to klines endopoint for recent klines
    *mostly for testing purposes

    params
    ------
    symbol: str
        symbol for trading pair
    interval: str
        eg. '15m' in binance api format, more below
    output: str
        return the whole response or just the data
        *'dataframe' default, 'test' to get entire response for testing purposes*

    *binance interval options:
    1s, [1,3,5,15,30]m, [1,2,4,6,8,12]h, [1,3]d, 1w, 1M
    '''
    if 'klines' not in binance_api_endpoints:
        print("No 'klines' API endpoint on record")
        return -1
    
    response = requests.get(url=binance_url + binance_api_endpoints['klines'], params={'symbol':symbol, 'interval': interval})

    if not _status(response):
        return -1
    
    if output == 'test':
        return response
    
    elif output == 'dataframe':

        data = pd.DataFrame(json.loads(response.text))
        data.columns = binance_klines_labels
        data = data.set_index('open time')
        data = data.astype('float')
        return data.drop(columns=["unused", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume"])
        

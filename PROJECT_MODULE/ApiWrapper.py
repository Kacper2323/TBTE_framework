import requests
import json
import pandas as pd

class CallWrapper:

    '''
    Class for performing API calls to binance servers.

    params
    ------
    url: str
        url of the REST API
    apiCalls: dict
        API endpoints for desired operations eg. {'time': '/api/v3/time', ...}
        currently supports: Binance: [klines, time]
    '''

    def __init__(self, url: str, apiCalls: dict) -> None:
        self.url = url
        self.apiCalls = apiCalls


    def _status(self, api_response):
        
        value = api_response.status_code
        match value:
            case 404:
                print("Resource not found ({})".format(value))
                return 0
            case 429 | 418 | 403:
                print("You have been PURGED. ATONE FOR YOUR SINS!! {}".format(value))
                return 0
            case 200:
                return 1
            case _:
                print("Unknown exit status code: {}".format(value))
                return 0


    def get_server_time(self):

        if 'time' not in self.apiCalls:
            print("No 'time' API endpoint on record.")
            return -1
        
        response = requests.get(self.url + self.apiCalls['time'])

        if not self._status(response):
            return -1
        return response


    def get_recent_klines(self, symbol: str, interval: str, output='dataframe') -> pd.DataFrame:
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
        if 'klines' not in self.apiCalls:
            print("No 'klines' API endpoint on record")
            return -1
        
        response = requests.get(url=self.url + self.apiCalls['klines'], params={'symbol':symbol, 'interval': interval})

        if not self._status(response):
            return -1
        
        if output == 'test':
            return response
        
        elif output == 'dataframe':

            data = pd.DataFrame(json.loads(response.text))
            data.columns = ["open time", "Open", "High", "Low", "Close", "Volume",
                "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume",
                "Taker buy quote asset volume", "unused"]
            data = data.set_index('open time')
            data = data.astype('float')
            return data.drop(columns=["unused", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume"])
            
import json
import base64
import time
import requests
import pandas as pd
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class BinanceClient:

    '''
    Used to communicate with Binance API. Utilizes requests library.
    If instantiated without parameters will fall back on default values:

    *default url = 'https://data-api.binance.vision', only GET requests available

    params
    ------
    url: str
        url of the API
    api_key: str
    private_key_path: str
        path to a .pem file containing a private key
    PK_password: str
        password to the private key file, if any (though strongly recommended)
    '''

    def __init__(self, 
                 url: str=None, 
                 api_key: str=None,
                 private_key_path: str=None,
                 PK_password: str=None
                 ) -> None:
        
        self.binance_url = url or 'https://data-api.binance.vision'
        self.API_KEY = api_key
        self.PRIVATE_KEY = None

        if private_key_path:
            with open(private_key_path, 'rb') as f:
                self.PRIVATE_KEY = load_pem_private_key(data=f.read(), password=PK_password)

        
        
    binance_api_endpoints = {'time': '/api/v3/time', 
                            'klines': '/api/v3/klines',
                            'price': '/api/v3/avgPrice', 
                            'orderBook': '/api/v3/depth',
                            'info': '/api/v3/exchangeInfo', 
                            'ping': '/api/v3/ping',
                            'ticker': '/api/v3/ticker', 
                            'ticker24h': '/api/v3/ticker/24hr',
                            'orderBookTicker': '/api/v3/ticker/bookTicker', 
                            'tickerPrice':'/api/v3/ticker/price',
                            'trades': '/api/v3/trades'}

    binance_klines_labels = ["open time", 
                            "Open", 
                            "High", 
                            "Low", 
                            "Close", 
                            "Volume",
                            "Close time", 
                            "Quote asset volume", 
                            "Number of trades", 
                            "Taker buy base asset volume",
                            "Taker buy quote asset volume", 
                            "unused"]


    def addKeys(self, api_key: str, private_key_path: str=None, PK_password: str=None) -> bool:
        '''
        Add api and private keys to the instance.

        params
        ------
        api_key: str
        private_key_path: str
            path to the .pem file
        PK_password: str
            password to the private key file, if any

        returns
        -------
        bool:
            1 if succeded, 0 if failed, the reason for failure may include keys already existing
        '''
        _retVal = 0
        if not self.api_key:
            self.API_KEY = api_key
            _retVal = 1
            
        if private_key_path and not self.PRIVATE_KEY: 
            with open(private_key_path, 'rb') as f:
                self.PRIVATE_KEY = load_pem_private_key(data=f.read(), password=PK_password)
            _retVal = 1
        
        print("keys already loaded")
        return _retVal


    def _status(aelf, api_response: requests.Response) -> int:
        
        '''
        returns 1 when status code is 200, 0 otherwise
        '''

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


    def GET(self, resource: str, params: dict=None) -> requests.Response:

        if self.PRIVATE_KEY:
            headers = {'X-MBX-APIKEY': self.API_KEY}
            response = requests.get(self.binance_url + self.binance_api_endpoints[resource], params=params, headers=headers)

        else:
            response = requests.get(self.binance_url + self.binance_api_endpoints[resource], params=params)

        return response


    def get_server_time(self) -> requests.Response:

        if 'time' not in self.binance_api_endpoints:
            print("No 'time' API endpoint on record.")
            return -1
        
        response = requests.get(self.binance_url + self.binance_api_endpoints['time'])

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
        
        returns
        -------
        pd.DataFrame with 500 last klines

        note
        ----
        binance interval options:
        1s, [1,3,5,15,30]m, [1,2,4,6,8,12]h, [1,3]d, 1w, 1M
        '''

        if 'klines' not in self.binance_api_endpoints:
            print("No 'klines' API endpoint on record")
            return -1
        
        response = requests.get(url=self.binance_url + self.binance_api_endpoints['klines'], params={'symbol':symbol, 'interval': interval})

        if not self._status(response):
            return -1
        
        if output == 'test':
            return response
        
        elif output == 'dataframe':

            data = pd.DataFrame(json.loads(response.text))
            data.columns = self.binance_klines_labels
            data = data.set_index('open time')
            data = data.astype('float')
            return data.drop(columns=["unused", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume"])
            

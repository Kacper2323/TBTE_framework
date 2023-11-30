binance_url = 'https://data-api.binance.vision'

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


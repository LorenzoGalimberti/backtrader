from urllib import response
import requests
import csv
import pandas as pd

api='Q0BN13I1CM925WG7'
interval='15min'
data_type='json'
#data_type='csv'
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval={interval}&outputsize=full&datatype={data_type}&apikey={api}'
r = requests.get(url)
data=r.json()
data=pd.DataFrame(data)
print(len(data))
import yfinance as yf
import numpy as np
import pandas as pd
import time 
tag='ETH-USD'
ticker= yf.Ticker(tag)
data= ticker.history (period="700d" ,interval="1d") # period="60d" , start=, end="2020-06-07"
try:
    del data['Dividends']
    del data['Stock Splits']
except: None

data['Date']=data.index

data.set_index(data.Date, inplace=True)
#data.to_csv(f'data\{tag}.csv')
data.to_csv(f'data\{tag}.csv',date_format="%Y-%m-%d %H:%M:%S")
data_saved_file = pd.read_csv(f'data\{tag}.csv')
data_saved_file

from email.quoprimime import quote
import alpaca_trade_api as tradeapi
import config
from datetime import date, datetime
from alpaca_trade_api.rest import TimeFrame,TimeFrameUnit
import pandas as pd

# ESTRAZIONE DATI

def extract(list):
    elem_list=[]
    for elem in list:
        elem_list.append(elem)
    return elem_list        


# configurtion of alpaca api
api=tradeapi.REST(config.API_KEY,config.API_SECRET)
tag='ETHUSD'
#date='2022-03-10'
oggi=date.today()

bars=api.get_crypto_bars(tag,TimeFrame(60, TimeFrameUnit.Minute),start="2021-09-01", limit=10000, exchanges='CBSE').df
#quotes=api.get_crypto_quotes(tag,"202cbse1-06-08", "2021-06-09").df #gets the quotes --> 
bars=pd.DataFrame(bars)
df=pd.DataFrame(columns=['Date','Open','High','Low','Close','Volume'],index=None)

df['Date']=bars.index
df['Open']=extract(bars.open)
df['High']=extract(bars.high)
df['Low']=extract(bars.low)
df['Close']=extract(bars.close)
df['Volume']=extract(bars.volume)

df.to_csv(f'data/{tag}.csv',date_format="%Y-%m-%d %H:%M:%S")
data_saved_file = pd.read_csv(f'data/{tag}.csv')
data_saved_file

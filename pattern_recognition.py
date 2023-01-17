import talib
import yfinance as yf
import numpy as np
tag='SPY'
data=yf.download(tag,start='2020-01-01',end='2020-08-01')

morning_star = talib.CDLMORNINGSTAR(data['Open'],data['High'],data['Low'] ,data['Close'])
engulfing=talib.CDLENGULFING(data['Open'],data['High'],data['Low'] ,data['Close'])
evening_star=talib.CDLEVENINGSTAR(data['Open'],data['High'],data['Low'] ,data['Close'])
averagedirindex=talib.ADX(data.High,data.Low,data.Close)

data['morning star']=morning_star
data['engulfing']=engulfing
macd=talib.MACD(data['Close']-data['Close'])
#print(engulfing[engulfing !=
print(averagedirindex)
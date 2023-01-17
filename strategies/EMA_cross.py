"""EMA - CROSS -RSI     stato indicatore: acerbo
- non per il forex
-cercare di capire la relazione fra la larghezza delle medie e la volatilità'
- capire se vendere tanto prima o dopo 

"""

from __future__ import print_function
import backtrader as bt
from datetime import datetime
# INSERT STOP LOSSES
class EmaCross(bt.Strategy):
   
    # list of parameters which are configurable for the strategy
    params=(('very_fast',9),('fast',11),('slow',45),('order_percentage',0.99),('ticker','BTC-USD'))
    name= 'Ema Cross'
    stop_loss=0.99
    def __init__(self):
        self.val_start=self.broker.get_cash()
        #self.mom =bt.talib.MOM(self.data.close, timeperiod=14)
        #macd= bt.talib.MACD(self.data.close, fastperiod=12, slowperiod=26, signalperiod=9)
        #real = bt.talib.DX(self.data.high, self.data.low, self.data.close, timeperiod=50)
        #self.stoch = bt.talib.STOCH(self.data.high, self.data.low, self.data.close,fastk_period=20, slowk_period=50, slowk_matype=0, slowd_period=20, slowd_matype=0)
        #aaron=bt.talib.AROON(self.data.high,self.data.low,timeperiod=50)
        #self.rsi=bt.talib.RSI(self.data.close,timeperiod=100)
        self.very_fast_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.very_fast,plotname=f'{self.params.very_fast} day moving avarage'
        )
        self.fast_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.fast,plotname=f'{self.params.fast}  day moving avarage'
        )
        self.slow_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.slow,plotname=f'{self.params.slow} day moving avarage'
        )
        self.crossover = bt.indicators.CrossOver(self.fast_moving_average,self.slow_moving_average)
        self.crossover2 = bt.indicators.CrossOver(self.very_fast_moving_average,self.slow_moving_average)

    def next(self):
        if  self.position.size==0:  # not in the market
             if self.crossover > 0 :  # if fast crosses slow to the upside
                amount_to_invest= (self.params.order_percentage*self.broker.cash)
                #self.size= math.floor(amount_to_invest/self.data.close)
                self.size= amount_to_invest/self.data.close  # quando anche frazioni 

                #self.stoploss=self.stop_loss  #stop-loss a 1%
                self.stop_price= (self.data.close)*self.stop_loss 
                

                print("buy {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.stop_price >= self.data.close :
                print("sell {} shares of {} at {} with stop loss ".format(self.size,self.params.ticker,self.data.close[0])) 
                self.close(size=self.size)
            elif self.crossover2 < 0  :

                molt=0.1 #uguali
                #self.close(size=self.size)
                #if self.rsi > 55:
                 #   molt=0.9
                #else:
                 #   molt=0.1


                self.size2=self.size*molt
                print("sell {} shares of {} at {} ".format(self.size2,self.params.ticker,self.data.close[0]))
                self.close(size=self.size2)
                self.remain_size=self.size-self.size2
                self.size=self.remain_size
            elif self.crossover <0:
                print("sell {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 
                #self.close(size=self.size)
                self.close(size=self.size)

                

    def stop(self):
        self.roi=(self.broker.get_value()/self.val_start)-1
        print('strategy : {} ROI :{:.2f}%  '.format(self.name,self.roi*100.00))
        
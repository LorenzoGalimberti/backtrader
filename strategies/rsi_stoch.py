from __future__ import print_function
import backtrader as bt
from datetime import datetime
# INSERT STOP LOSSES
class Rsi_Stoch(bt.Strategy):
   
    # list of parameters which are configurable for the strategy
    params=(('very_fast',200),('fast',11),('slow',45),('order_percentage',0.99),('ticker','BTC-USD'))
    name= 'Ema Cross'
    stop_loss=0.99
    def __init__(self):
        self.val_start=self.broker.get_cash()
        self.macd=bt.talib.MACD(self.data.close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.rsi=bt.talib.RSI(self.data.close,timeperiod=14)
        self.stoch_rsi=bt.talib.STOCHRSI(self.data.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.stoch=bt.talib.STOCH(self.data.high,self.data.low,self.data.close,  fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    def next(self):
        if  self.position.size==0:  # not in the market
             if self.rsi <30 :  # if fast crosses slow to the upside
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
            elif self.rsi >70  :
                print("sell {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0]))
                self.close(size=self.size)
            

                

    def stop(self):
        self.roi=(self.broker.get_value()/self.val_start)-1
        print('strategy : {} ROI :{:.2f}%  '.format(self.name,self.roi*100.00))
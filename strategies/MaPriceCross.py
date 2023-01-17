from __future__ import print_function
import backtrader as bt
from datetime import datetime

class MaPriceCross(bt.Strategy):
   
    # list of parameters which are configurable for the strategy
    params=(('sma',50),('order_percentage',0.95),('ticker','BTC-USD'))
    name= 'MaPriceCross'
    def __init__(self):
        self.val_start=self.broker.get_cash()
        self.stop_price=0 
        sma1 = bt.ind.SMA(period=self.params.sma)  # simple moving average
        self.crossover = bt.ind.CrossOver(self.data.close,sma1)  # crossover signal
        return self.name
    
    def next(self):
        if  self.position.size==0:  # not in the market
             if self.crossover > 0:  # if fast crosses slow to the upside
                amount_to_invest= (self.params.order_percentage*self.broker.cash)
                #self.size= math.floor(amount_to_invest/self.data.close)
                self.size= amount_to_invest/self.data.close  # quando anche frazioni 
                
                self.stoploss=0.99  #stop-loss a 1%
                self.stop_price= (self.data.close)*self.stoploss 
                
                
                print("buy {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 
                self.buy(size=self.size)

        if self.position.size > 0:
        
            if self.stop_price >= self.data.low :
                print("sell {} shares of {} at {} with stop loss ".format(self.size,self.params.ticker,self.data.low[0])) 
                self.close(size=self.size)
            elif self.crossover < 0 :
                print("sell {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 
                self.close(size=self.size)
    
    def stop(self):
        self.roi=(self.broker.get_value()/self.val_start)-1
        print('strategy : {} ROI :{:.2f}%   S/L : {:.2f}%  SMA : {}'.format(self.name,self.roi*100.00,(1- self.stoploss)*100.00,self.params.sma))
        
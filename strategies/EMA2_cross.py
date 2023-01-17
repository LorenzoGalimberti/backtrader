from __future__ import print_function
import backtrader as bt
from datetime import datetime
# INSERT STOP LOSSES
class EmaCross2(bt.Strategy):
   
    # list of parameters which are configurable for the strategy
    params=(('fast',10),('slow',430),('very_slow',800),('order_percentage',0.95),('ticker','BTC-USD'),('stop_loss',0.99))
    name= 'Ema2 Cross'
    #stop_loss=0.99
    
    def __init__(self):
  
        self.val_start=self.broker.get_cash()
        
       
        self.fast_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.fast,plotname=f'{self.params.fast}  day moving avarage'
        )
        self.slow_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.slow,plotname=f'{self.params.slow} day moving avarage'
        )
        self.very_slow_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.very_slow,plotname=f'{self.params.very_slow} day moving avarage'
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average,self.slow_moving_average)
        self.crossover2 = bt.indicators.CrossOver(self.fast_moving_average,self.very_slow_moving_average)
        

    def next(self):
        if  self.position.size==0:  # not in the market
             if self.crossover >0 :  # if fast crosses slow to the upside
                amount_to_invest= (self.params.order_percentage*self.broker.cash)
                #self.size= math.floor(amount_to_invest/self.data.close)
                self.size= amount_to_invest/self.data.close  # quando anche frazioni 
                print("buy {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 
                #self.stoploss=self.stop_loss  #stop-loss a 1%
                self.stop_price= (self.data.close[0])*self.params.stop_loss
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.stop_price >= self.data.close :
                print("sell {} shares of {} at {} with stop loss ".format(self.size,self.params.ticker,self.data.close[0])) 
                self.close(size=self.size)
            elif self.crossover < 0  :
                print("sell {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0]))
                self.close(size=self.size)
            

                

    def stop(self):
        self.roi=(self.broker.get_value()/self.val_start)-1
        print('strategy : {} ROI :{:.2f}%  '.format(self.name,self.roi*100.00))
        
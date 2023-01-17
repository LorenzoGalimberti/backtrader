from __future__ import print_function
import backtrader as bt
from datetime import datetime
import statistics as stat

# INSERT STOP LOSSES
class CashTrap(bt.Strategy):
    
    name='BBands'
    params = (
    ("period", 18),
    ("devfactor", 2),
    ("size", 20),
    ("debug", False),
    ('order_percentage',0.95),
    ('fast',200)
    )
 
    def __init__(self):
        self.stop_loss=0.99
        self.val_start=self.broker.get_cash()
        self.fast_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.fast,plotname=f'{self.params.fast}  day moving avarage'
        )
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.mid)
        self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)
        self.rsi=bt.talib.RSI(self.data.close ,timeperiod=5)
    def next(self):
        if  self.position.size==0:  # not in the market
             if self.lx > 0 and self.fast_moving_average < self.data.close and self.rsi <35 :  # if fast crosses slow to the upside
                amount_to_invest= (self.params.order_percentage*self.broker.cash)
                #self.size= math.floor(amount_to_invest/self.data.close)
                self.size= amount_to_invest/self.data.close  # quando anche frazioni 

                #self.stoploss=self.stop_loss  #stop-loss a 1%
                self.stop_price= (self.data.close[0])*self.stop_loss 
                

                print("buy {} shares at {} ".format(self.size,self.data.close[0])) 
                self.buy(size=self.size)

        if self.position.size > 0:
           
                self.close(size=self.size)
            
    def stop(self):
        self.roi=(self.broker.get_value()/self.val_start)-1
        print('strategy : {} ROI :{:.2f}%  '.format(self.name,self.roi*100.00))
                
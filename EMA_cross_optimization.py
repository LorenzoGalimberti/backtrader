from __future__ import print_function
import backtrader as bt
from datetime import datetime
import yfinance as yf
from unicodedata import name
from matplotlib import style
#import backtrader.analyzers as btanalyzers
import numpy as np
import pandas as pd
# INSERT STOP LOSSES
class EmaCross(bt.Strategy):
   
    # list of parameters which are configurable for the strategy
    params=(('very_fast',7),('fast',10),('slow',50),('order_percentage',0.95),('stop_loss',0.99),('molt',0.1))#
    name= 'Ema Cross'
   
    def __init__(self):
        
        self.val_start=self.broker.get_cash()
        
        self.very_fast_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.very_fast)
        self.fast_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.fast)
        self.slow_moving_average=bt.indicators.EMA(
            self.data.close,period= self.params.slow)
        
        self.crossover = bt.indicators.CrossOver(self.fast_moving_average,self.slow_moving_average)
        self.crossover2 = bt.indicators.CrossOver(self.very_fast_moving_average,self.slow_moving_average)
        
    def next(self):
        if  self.position.size==0:  # not in the market
             if self.crossover > 0 :  # if fast crosses slow to the upside
                amount_to_invest= (self.params.order_percentage*self.broker.cash)
                #self.size= math.floor(amount_to_invest/self.data.close)
                self.size= amount_to_invest/self.data.close  # quando anche frazioni 

                
                self.stop_price= (self.data.close)*self.params.stop_loss 
                

                #print("buy {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.stop_price >= self.data.close :
                #print("sell {} shares of {} at {} with stop loss ".format(self.size,self.params.ticker,self.data.close[0])) 
                self.close(size=self.size)
            elif self.crossover2 < 0  :

                 #uguali
                #self.close(size=self.size)
                #if self.rsi > 55:
                 #   molt=0.9
                #else:
                 #   molt=0.1


                self.size2=self.size*self.params.molt
                #print("sell {} shares of {} at {} ".format(self.size2,self.params.ticker,self.data.close[0]))
                self.close(size=self.size2)
                self.remain_size=self.size-self.size2
                self.size=self.remain_size
            elif self.crossover <0:
                #print("sell {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 
                #self.close(size=self.size)
                self.close(size=self.size)

                

    def stop(self):
        self.roi=(self.broker.get_value()/self.val_start)-1
        print('very fast : {} fast : {} slow : {} -- ROI :{:.2f}% --S/L={:.3f}% -- molt ={}  '.format(self.params.very_fast,self.params.fast,self.params.slow,self.roi*100.00,self.params.stop_loss,self.params.molt))#-- molt : {} ,self.params.molt
        

if __name__=='__main__':
    cerebro=bt.Cerebro()
    cerebro.broker.setcash(1000)

    spy_prices= pd.read_csv('data/ETH-USD.csv',index_col='Date',parse_dates=True)
    feed=bt.feeds.PandasData(dataname= spy_prices)
    cerebro.adddata(feed)

    #cerebro.addstrategy(SampleStrategy)
    cerebro.optstrategy(EmaCross,fast=range(14,21),slow=range(70,100,2),very_fast=range(7,10),molt=[0.01,0.02,0.03,0.04,0.05,0.07,0.08])# ,molt=range(0,1,0.05)
    cerebro.broker.setcash(10000)
    #cerebro.addsizer(bt.sizers.PercentSizer,percent=10)
    #cerebro.addanalyzer(btanalyzers.SharpeRatio,_name="sharpe",timeframe=bt.TimeFrame.Days)
    # ------ SET COMMISSION --------

    cerebro.broker.setcommission(commission=0.00075)

    backs=cerebro.run()
import backtrader as bt
from datetime import datetime

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params=(('fast',10),('slow',30),('order_percentage',0.95),('ticker','BTC-USD'))
    def __init__(self):
        sma1 = bt.ind.SMA(period=self.params.fast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.params.slow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                amount_to_invest= (self.params.order_percentage*self.broker.cash)
                #self.size= math.floor(amount_to_invest/self.data.close)
                self.size= amount_to_invest/self.data.close  # quando anche frazioni 

                print("buy {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 

                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                print("sell {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 
                self.close(size=self.size)

    
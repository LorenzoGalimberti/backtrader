from unicodedata import name
import backtrader as bt

class BuyHold(bt.Strategy):
    
    name='BUY AND HOLD STRATEGY'
    params=(('order_percentage',0.95),('ticker','BTC-USD'))

    def start(self):
        self.val_start=self.broker.get_cash()
    def next(self):
        if self.position.size == 0:
            amount_to_invest= (self.params.order_percentage*self.broker.cash)
            #self.size= math.floor(amount_to_invest/self.data.close)
            self.size= amount_to_invest/self.data.close  # quando anche frazioni 
            print("buy {} shares of {} at {} ".format(self.size,self.params.ticker,self.data.close[0])) 

            self.buy(size=self.size)
    def stop(self):
        self.roi=(self.broker.get_value()/self.val_start)-1
        print('starting value :{:,.2f} $'.format(self.val_start))
        print('ROI : {:.2f}%'.format(self.roi*100.00))
        print(self.name)
       
            
            
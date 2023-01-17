from __future__ import print_function
import backtrader as bt
from datetime import datetime


class SampleStrategy(bt.Strategy):
    params=(
        ('fast_length',5),
        ('slow_length',25)

    )

    def __init__(self):
        ma_fast=bt.ind.SMA(period=self.params.fast_length)
        ma_slow=bt.ind.SMA(period=self.params.slow_length)
        self.crossover=bt.ind.CrossOver(ma_fast,ma_slow)

    def next(self):
        if not self.position:
            if self.crossover >0:
                self.buy()
        if self.position:
            if self.crossover <0:
                self.close()
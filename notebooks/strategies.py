from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt

class SPY_Buy_and_Hold(bt.Strategy):

    def __init__(self):

        self.spy = self.datas[0]
        
    def log(self, txt, value1=None, value2=None, value3=None):
        
        print(f'{txt}') 
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %(order.executed.price, order.executed.value, order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %(order.executed.price,order.executed.value,order.executed.comm))
            self.bar_executed = len(self)
    
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
    
        # Reset orders
        self.order = None
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
    
        self.log('GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        
    def next(self):
        curr_dt = self.datas[0].datetime.date(0)

        spy_position = (self.getposition(self.spy).size>0)
        
        if (not spy_position): 
            self.buy(data=self.spy, size=None)
            self.log(f'{curr_dt} SPY BUY CREATED --- Price: {self.spy.close[0]:.2f} ')
                
class QQQ_SPY_Signal_Buy_and_Hold(bt.Strategy):
    params = (
        ('qqq_ma_period', 30),
        ('spy_fast_ma', 50),
        ('spy_slow_ma', 200),
    )
    def __init__(self):
        self.qqq = self.datas[0]
        self.spy = self.datas[1]
        self.qqq_ma = bt.indicators.SimpleMovingAverage(self.qqq, period=self.p.qqq_ma_period)
        self.spy_fast_ma = bt.indicators.SimpleMovingAverage(self.spy, period=self.p.spy_fast_ma)
        self.spy_slow_ma = bt.indicators.SimpleMovingAverage(self.spy, period=self.p.spy_slow_ma)

        self.qqq_cross = bt.indicators.CrossOver(self.qqq, self.qqq_ma)
        self.spy_cross = bt.indicators.CrossOver(self.spy_fast_ma, self.spy_slow_ma)
        
    def log(self, txt, value1=None, value2=None, value3=None):
        
        print(f'{txt}') 
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %(order.executed.price, order.executed.value, order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %(order.executed.price,order.executed.value,order.executed.comm))
            self.bar_executed = len(self)
    
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
    
        # Reset orders
        self.order = None
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
    
        self.log('GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        
    def next(self):
        curr_dt = self.datas[0].datetime.date(0)
        qqq_position = (self.getposition(self.qqq).size>0)
        spy_position = (self.getposition(self.spy).size>0)
        
        if (not qqq_position) and (not spy_position): 
            if (self.qqq_cross > 0) | (self.qqq_cross[-1] > 0) :  # Nasdaq 100 crosses above 30-day MA on curr or prev day

                self.buy(data=self.qqq, size=None)

                self.log(f'{curr_dt} QQQ BUY CREATED --- Price: {self.qqq.close[0]:.2f} ') 
                #print("qqq position: "+ str(self.order))

            elif (self.spy_cross > 0) | (self.spy_cross[-1] > 0):    # S&P 500 Golden Cross
                self.buy(data=self.spy, size=None)
                self.log(f'{curr_dt} SPY BUY CREATED --- Price: {self.spy.close[0]:.2f} ')

class QQQ_SPY_SMA(bt.Strategy):
    params = (
        ('qqq_ma_period', 30),
        ('spy_fast_ma', 50),
        ('spy_slow_ma', 200),
    )

    def __init__(self):
        self.qqq = self.datas[0]
        self.spy = self.datas[1]
        self.gld = self.datas[2]

        self.qqq_ma = bt.indicators.SimpleMovingAverage(self.qqq, period=self.p.qqq_ma_period)
        self.spy_fast_ma = bt.indicators.SimpleMovingAverage(self.spy, period=self.p.spy_fast_ma)
        self.spy_slow_ma = bt.indicators.SimpleMovingAverage(self.spy, period=self.p.spy_slow_ma)

        self.qqq_cross = bt.indicators.CrossOver(self.qqq, self.qqq_ma)
        self.spy_cross = bt.indicators.CrossOver(self.spy_fast_ma, self.spy_slow_ma)

    def log(self, txt, value1=None, value2=None, value3=None):
        pass
        # print(f'{txt}') 
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %(order.executed.price, order.executed.value, order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %(order.executed.price,order.executed.value,order.executed.comm))
            self.bar_executed = len(self)
    
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
    
        # Reset orders
        self.order = None
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
    
        self.log('GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        
    def next(self):
        curr_dt = self.datas[0].datetime.date(0)
        qqq_position = (self.getposition(self.qqq).size>0)
        gld_position = (self.getposition(self.gld).size>0)
        spy_position = (self.getposition(self.spy).size>0)
        
        # if not self.position: # if there's no position
        if (not qqq_position) and (not gld_position) and (not spy_position): 
            if (self.qqq_cross > 0) | (self.qqq_cross[-1] > 0) :  # Nasdaq 100 crosses above 30-day MA on curr or prev day

                # if self.qqq_cross <0:
                #     pass
                # else:
                self.buy(data=self.qqq, size=None)

                self.log(f'{curr_dt} QQQ BUY CREATED --- Price: {self.qqq.close[0]:.2f} ') 
                #print("qqq position: "+ str(self.order))

            elif (self.spy_cross > 0) | (self.spy_cross[-1] > 0):   # S&P 500 Golden Cross
                # if self.spy_cross <0:
                #     pass
                # else:
                self.buy(data=self.spy, size=None)
                self.log(f'{curr_dt} SPY BUY CREATED --- Price: {self.spy.close[0]:.2f} ')
            
            elif (self.qqq_cross[-1] < 0) | (self.spy_cross[-1] < 0):
                
                # print("Portfolio value: "+str(self.broker.getvalue()))
                self.buy(data=self.gld, size=None) # , tradeid=self.curtradeid
                self.log(f'{curr_dt} GLD BUY CREATED --- Price: {self.gld.close[0]:.2f} ')
                
        else:
            
            if qqq_position:
                # if self.qqq_cross < 0:  # Nasdaq 100 crosses below 30-day MA
                if (self.qqq_cross < 0) | (self.qqq_cross[-1] < 0):
                    # self.order = self.qqq.order_target_percent(target=0)
                    self.close(data=self.qqq, size=None) # , tradeid=self.curtradeid
                    self.log(f'{curr_dt} QQQ SELL CREATED --- Price: {self.qqq.close[0]:.2f} ')
                    
                    
            elif spy_position:
                # if self.spy_cross < 0:  # S&P 500 Death Cross
                if (self.spy_cross < 0) | (self.spy_cross[-1] < 0):
                    self.close(data=self.spy, size=None)
                    self.log(f'{curr_dt} SPY SELL CREATED --- Price: {self.spy.close[0]:.2f} ')

            elif gld_position:
                if self.qqq_cross > 0:
                    self.close(data=self.gld, size=None)
                    self.log(f'{curr_dt} GLD SELL CREATED --- Price: {self.gld.close[0]:.2f} ')

                elif self.spy_cross > 0:
                    self.close(data=self.gld, size=None)
                    self.log(f'{curr_dt} GLD SELL CREATED --- Price: {self.gld.close[0]:.2f} ')

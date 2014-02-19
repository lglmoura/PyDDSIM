'''
Created on 24/04/2010

@author: Luiz Gustavo
'''

from pydssim.peer.trading.abstract_trading import AbstractTrading

class TradingService(AbstractTrading):
    '''
    classdocs
    '''

    def __init__(self,snow,service,periodStart,periodEnd,quantity,type):
        '''
        Constructor
        '''
        self.initialize(snow,service,periodStart,periodEnd,quantity,type)
        
    def initialize(self,snow, service,periodStart,periodEnd,quantity,type):
        AbstractTrading.initialize(self,snow, service,periodStart,periodEnd,quantity,type)
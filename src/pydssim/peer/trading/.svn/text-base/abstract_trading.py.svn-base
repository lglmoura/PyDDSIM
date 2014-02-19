'''
Created on 28/08/2009

@author: LGustavo

'''


from pydssim.util.decorator.public import  createURN
from pydssim.util.data_util import randomDate
from random import random,randint
from pydssim.util.log.trading_logger import TradingLogger
from multiprocessing import Semaphore


class AbstractTrading():
    '''
    classdocs
    '''
    STARTED     = "0001"
    COMPLETE    = "0002" # vencedor
    NOTCOMLETE  = "0003" # nao venceu
    ACK         = "0004"
    NULL        = "0000"
    
    CLIENT      = "1000"
    SERVER      = "1001"
  
    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def initialize(self, service,periodStart,periodEnd,quantity,type=CLIENT,metric="MB"):
      
        self.__uuid = createURN("trading")
        self.__service = service
        self.__periodStart = periodStart
        self.__periodEnd = periodEnd
        self.__quantity = quantity
        self.__metric   = metric
        
        self.__status   = AbstractTrading.STARTED
        self.__attempt  = 1
        self.__type     = type
        
        
        self.__peersTrading = {}
         
        
        TradingLogger().resgiterLoggingInfo("Initialize Trading = URN = %s,"%(self.__uuid))
    
    
    def getType(self):
        return self.__type
    
    
    def setOwnershipCertificate(self,ownershipCertificate):
        
        sharedPeriods = self.getService().hasSharePeriods(self.__periodStart,self.__periodEnd)
        sharedPeriodid,share = sharedPeriods.popitem()
        share.setOwnerCertificate(ownershipCertificate)
        self.getService().updateSharePeriod(share)  
        
    def getAttempt(self):
        return self.__attempt
    
    def setAttempt(self,attempt):
        self.__attempt = attempt
    
    def definyPeerTrading(self):
        
        value =0;
        peerAux =""
        semaphore = Semaphore()
        semaphore.acquire()
        for peer,trust in self.__peersTrading.iteritems():
            
            if trust >= value:
                value = trust
                peerAux = peer 
            
            
        semaphore.release()
        return (peerAux,value)

    def getPeersTrading(self):
        return self.__peersTrading
    
    def addPeerTrading(self,peer,trust):
        
        self.__peersTrading[peer] = trust 
    
    def setEquivalence(self,equivalence):
        self.__equivalence = equivalence
        
    def getEquivalence(self):
        return self.__equivalence
    
    def getMetric(self):
        return self.__metric
        
    def setQuantityEquivalence(self,quantity):
        self.__quantityEquivalnce = quantity
        
    def getQuantityEquvalence(self):
        return self.__quantityEquivalnce    
        
        
    def getUUID(self):
        return self.__uuid 
    
    def setUUID(self,uuid):
        self.__uuid = uuid
          
    def getService(self):
        return self.__service
    
    def getPeriodStart(self):
        return self.__periodStart
    
    def getPeriodEnd(self):
        return self.__periodEnd
    
    def getPeriods(self):
        return (self.__periodStart,self.__periodEnd)
    
    def getQuantity(self):
        return self.__quantity
    
    def getStatus(self):
        return self.__status
    
    def setStatus(self,status):
        self.__status = status
     
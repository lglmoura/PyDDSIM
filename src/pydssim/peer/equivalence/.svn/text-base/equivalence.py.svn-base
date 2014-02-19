'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.util.decorator.public import  createURN
from pydssim.util.log.equivalence_logger import EquivalenceLogger

class Equivalence(object):
    
    
    def __init__(self,service,serviceQuantity,equivalence,equivalenceQuantity,periodStart,periodEnd):
        '''
        Constructor
        period = randomDate("1/1/2010 1:30", "1/12/2010 4:50", random())
        
        '''
        self.__uuid = createURN("equivalence")
        self.__service = service
        self.__serviceQuantity = serviceQuantity
        self.__equivalenceS     = equivalence
        self.__equivalenceQuantity = equivalenceQuantity
        self.__periodStart = periodStart
        self.__periodEnd   = periodEnd 
        
        EquivalenceLogger().resgiterLoggingInfo("Create Equivalence between %s and = %s periodStar = %s and periodEnd = %s"%self.getAllNeed())
    
    def getServiceQuantity(self):
        return self.__serviceQuantity
    
    def getEquivalenceQuantity(self):
        return self.__equivalenceQuantity
    
    def getService(self):
        return self.__service
    
    def getEquivalence(self):
        return self.__equivalenceS
    
    def getPeriodStart(self):
        return self.__periodStart
    
    def getPeriodEnd(self):
        return self.__periodEnd
    
    def getPeriodAll(self):
        return (self.getPeriodStart(),self.getPeriodEnd())
    
    def getAllNeed(self):
        return (self.__service,self.__equivalenceS,self.__periodStart,self.__periodEnd)
    
    def getUUID(self):
        return self.__uuid
        
            
        
         
            
    
    
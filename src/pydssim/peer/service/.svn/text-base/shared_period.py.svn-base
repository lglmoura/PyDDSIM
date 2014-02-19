'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.util.decorator.public import  createURN

class SharePeriod():
    
    '''
    classdocs
    
    
    '''
    
    IDLE  = 1
    SHARE = 2
    TRADING = 3
    NULL   = 0


    def __init__(self,service,periodStart,periodEnd,quantity,owner=createURN("ownershipCertificate"),metric="MB",status=IDLE):
        
        '''
        Constructor
        '''
        
        self.__uuid = createURN("shareservice")
        self.__ownershipCertificate = owner
        self.__service = service
        self.__periodStart = periodStart
        self.__periodEnd   = periodEnd
        self.__quantity    = quantity
        self.__metric      = metric
        self.__status      = status
        
       
    def getOwnerCertificate(self):
        return self.__ownershipCertificate
    
    def getService(self):
        return self.__service
    
    def setOwnerCertificate(self,ownershipCertificate):
        self.__ownershipCertificate = ownershipCertificate 
    
    def getMetric(self):
        return self.__metric
    
    def getQuantity(self):
        return self.__quantity
    
    def getStatus(self):
        return self.__status
    
    def setStatus(self,status):
        self.__status = status
    
   
    def getResource(self):
        return self.__resource
    
    
    def getPeriodStart(self):
        return self.__periodStart
    
    def getPeriodEnd(self):
        return self.__periodEnd
    
    def getUUID(self):
        return self.__uuid
        
        
        
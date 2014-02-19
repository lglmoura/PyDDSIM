'''
Created on 28/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''


from pydssim.util.decorator.public import  createURN
from pydssim.util.data_util import randomDate
from random import random,randint
from pydssim.util.log.trust_logger import TrustLogger


class AbstractTrust():
    '''
    classdocs
    '''
    
    DIRECT = "DIRECTTRUST"
    TRUSTF = "TRUSTFINAL"
    

    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def initialize(self, peerUUID,resourceUUID, resourceDescription , trustType= DIRECT ,rating =0.5, period = randomDate("1/1/2010 1:30", "1/12/2010 4:50", random()), status=False):
      
        self.__uuid = createURN(trustType)
        self.__resourceUUID = resourceUUID
        self.__resourceDescription = resourceDescription
        self.__peerUUID = peerUUID
        self.__rating = rating
        self.__period = period
        self.__status = status
        self.__trustType = trustType
        
        TrustLogger().resgiterLoggingInfo("Initialize Trust = URN = %s,Peer = %s ,Time %s, Description = %s rating = %f and status = %s"%(self.__uuid,self.__peerUUID,self.__period,self.__resourceDescription,self.__rating,self.__status))
     
        
    def getResourceDescription(self):
        return self.__resourceDescription 
    
      
    def getResourceUUID(self):
        return self.__resourceUUID
    
    
    def setResourceUUID(self,resource):
        self.__resourceUUID = resourceUUID
        return self.__resourceUUID
    
    def getPeerUUID(self):
        return self.__peerUUID
    
    def getTrustType(self):
        return self.__trustType
     
    def setPeerUUID(self,peer):
        self.__peer = peerUUID
        return self.__peerUUID
    
     
    def getRating(self):
        return self.__rating
        
    def getPeriod(self):
        return self.__period
    
    def getStatus(self):
        return self.__status
    
    def getUUID(self):
        return self.__uuid
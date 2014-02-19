'''
Created on 11/04/2010

@author: Luiz Gustavo
'''

import time
import threading
import traceback
from pydssim.peer.trading.information_service_agent import InformationServiceAgent
#from pydssim.util.data_util import strTime
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.peer.repository.tradings_repository import TradingsRepository
from pydssim.peer.trading.trading_service import TradingService
from pydssim.peer.trading.abstract_trading import AbstractTrading
from pydssim.peer.trading.information_service_agent import InformationServiceAgent
from random import random
from datetime import datetime
from pydssim.util.log.trading_logger import TradingLogger


class TradingManager(object):
    '''
    classdocs
    '''


    def __init__(self,peer):
        '''
        Constructor
        '''
        
        self.__peer = peer
        self.__tradings = TradingsRepository(peer)
        self.__isa= InformationServiceAgent(self)
        
    
    def getPeer(self):
        return self.__peer
        
    def getISA(self):
        return self.__isa
    
    def getTradings(self):
        return self.__tradings
    
    def creatTradingService(self,service,periodStart,periodEnd,quantity,type):
        TradingLogger().resgiterLoggingInfo("Initialize Trandig = URN = ,Peer = %s "%(self.__peer.getPID()))
        
        trading = TradingService(service,periodStart,periodEnd,quantity,type)
        
        self.createTrading(trading)
        
        return trading
    
    
    
    def setServiceForTrading(self,trading):
        
       
        TradingLogger().resgiterLoggingInfo("Set Service For Trading ,Peer = %s"%(self.__peer.getPID()))
        self.getTradings().addElement(trading)
        self.__isa= InformationServiceAgent(self)
        self.__isa.searchServiceForTrading(trading)
        
        tradingUUID = trading.getUUID()
        #print " trading 1 ", tradingUUID
        timeStart =time.time()
        
        peer = ""
        
        while (trading.getStatus() == AbstractTrading.STARTED and ((time.time() - timeStart) < 20)) :
            
            #print " trading 2 ", tradingUUID
            
            #trading = self.getTradings().getElementID(tradingUUID)
            #
            if trading.getStatus() == AbstractTrading.NOTCOMLETE:
                continue 
            
           
            if (time.time() - timeStart) > 10 and trading.getAttempt() == 1:
                #print "time --->>>", time.time()-timeStart, trading.getAttempt()
                timeStart =time.time()
                trading.setAttempt(trading.getAttempt() +1)
                self.__isa.searchServiceForTrading(trading)
                
            
           
            peer,trust = trading.definyPeerTrading()
            #print "num peer tra",trading.getUUID(),time.time() , timeStart,len(trading.getPeersTrading())
            if trust >= 0.5 or len(trading.getPeersTrading())>3:
                if self.__isa.sendResponseToPeerWinner(trading,self.getPeer().getPID(),peer)== AbstractTrading.ACK:
                    trading.setStatus(AbstractTrading.COMPLETE)
                   
                    ownershipCertificate = self.__isa.sendOwnershipCertificate(trading,self.getPeer().getURN(),peer)
                    trading.setOwnershipCertificate(ownershipCertificate)
                else:
                    trading.getPeersTrading().pop(peer)    
                    
                
        self.__isa.sendResponseToPeerAll(trading,self.getPeer().getPID(),peer)
        TradingLogger().resgiterLoggingInfo("****** Final Trading ,Peer = %s"%(self.__peer.getPID()))
        
    def createTrading(self,trading):
        
        try:        
            t = threading.Thread(target = self.setServiceForTrading,args=([trading]))
        
            t.start()
        except:
            
            traceback.print_exc()
                
        
        
        
        
        
'''
Created on 11/04/2010

@author: Luiz Gustavo
'''

import time
from pydssim.peer.repository.direct_trust_repository import DirectTrustRepository
from pydssim.peer.repository.trust_final_repository import TrustFinalRepository
#from pydssim.util.data_util import strTime
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from random import random
from datetime import datetime
from pydssim.peer.trust.trust_final import TrustFinal
from pydssim.peer.trust.abstract_trust import AbstractTrust

class TrustManager(object):
    '''
    classdocs
    '''


    def __init__(self,peer):
        '''
        Constructor
        '''
        
        self.__directTrust= DirectTrustRepository(peer)
        self.__trustFinal = TrustFinalRepository(peer)
        self.__peer = peer
        self.__gama = random() # peso de confDir
        self.__beta = 1 - self.__gama # peso da Rp
        #print "g b t",self.__gama,self.__beta, self.__gama+self.__beta
    
    
    def getPeer(self):
        return self.__peer
    
    def getGama(self):
        return self.__gama
    
    def getBeta(self):
        return self.__beta
        
    def getDirectTrust(self):
        return self.__directTrust
    
    def getTrustFinal(self):
        return self.__trustFinal
        
    def getTrustFinalValue(self,peerID,service,startDate,stopDate):
        
        trustFinals = self.getTrustFinal().getElements()
        
        transaction = 0.0
        totalTransaction = 0.0
        trustValueFinal = 0.1
        
        for key in trustFinals.keys():
            
            trustFinal = trustFinals[key]
            
            #print directTrust.getResourceDescription(),startDate,directTrust.getPeriod(),stopDate,(startDate<=directTrust.getPeriod()<=stopDate)
            
            if ((trustFinal.getPeerUUID() == peerID) and (startDate<=trustFinal.getPeriod()<=stopDate) and (trustFinal.getResourceDescription() == service)):
                #print peerID,service,startDate,stopDate
                #print " "
                totalTransaction+=1
                transaction+=trustFinal.getRating()
                        
                
        if totalTransaction != 0:        
            #print "----------->",transaction,totalTransaction,rating,nRating,float(transaction/totalTransaction),(rating/nRating)
            trustValueFinal = transaction/totalTransaction       
        
        return trustValueFinal
    
        
    
        
    def directTrustCalculation(self,peerID,service,startDate,stopDate):
        
        peerConf  = 0.0
        rating    = 0.0
        nRating   = 0
        
        directTrusts = self.getDirectTrust().getElements()
        
        transaction = 0.0
        totalTransaction = 0.0
        sConfDir = 0.1
        
        
        
        for key in directTrusts.keys():
            
            directTrust = directTrusts[key]
            
            #print directTrust.getResourceDescription(),startDate,directTrust.getPeriod(),stopDate,(startDate<=directTrust.getPeriod()<=stopDate)
            
            if ((directTrust.getPeerUUID() == peerID) and (startDate<=directTrust.getPeriod()<=stopDate)):
                #print peerID,service,startDate,stopDate
                #print " "
                totalTransaction+=1
                if directTrust.getStatus() == True:
                    transaction +=1
                    if directTrust.getResourceDescription() == service:
                        nRating +=1
                        rating += directTrust.getRating()
                        
                
        if nRating != 0:        
            #print "----------->",transaction,totalTransaction,rating,nRating,float(transaction/totalTransaction),(rating/nRating)
            sConfDir = ((transaction/totalTransaction)*(rating/nRating))       
        
        return (sConfDir,transaction,totalTransaction)
    
    
    
    def reputationCalculation(self,peerID,service,startDate,stopDate):
        
        peerConf  = 0.0
        rating    = 0.0
        nRating   = 0
        
        directTrusts = self.getDirectTrust().getElements()
        
        transaction = 0.0
        totalTransaction = 0.0
        reputation = 0.1
        
        neigbhors = {}       
        
        for key in directTrusts.keys():
            
            directTrust = directTrusts[key]
            
                       
            if ((directTrust.getPeerUUID() != peerID) and (startDate<=directTrust.getPeriod()<=stopDate)):
                
                
                if neigbhors.has_key(directTrust.getPeerUUID()):
                    
                    continue
                
                neigbhors[directTrust.getPeerUUID()] = directTrust
                
                sConfDir,transaction,totalTransaction = self.directTrustCalculation(directTrust.getPeerUUID(), service, startDate, stopDate)
                #print sConfDir,transaction,totalTransaction
                
                if totalTransaction != 0:
                    peerConf = transaction/totalTransaction
                
                host,port = directTrust.getPeerUUID().split(":")
                
                #print "--------------->",self.getPeer().getPID(),host,port,peerID, service, startDate, stopDate
                
                #self.getPeer().getPeerLock().acquire()             
                resp = self.getPeer().connectAndSend(host, port, AbstractMessageHandler.TRUSTFINAL, 
                        '%s %s %s %s' % (peerID, service, startDate, stopDate))#[0]
              
                #self.getPeer().getPeerLock().release()
                #print resp
                
                trustFinalValue = 0
                
                if resp != []:
                    #print "resp",resp,host,port 
                    trustFinalValue = float(resp[0][1])
                
                reputation+= (peerConf*trustFinalValue)
                
                #print "t e r",trustFinalValue, reputation
                #print " "
                
                        
                
        if len(directTrusts.keys()) != 0:        
            #print "----------->",reputation,len(directTrusts.keys())
            reputation = (reputation/len(directTrusts.keys()))       
        
        return reputation
    
    def TrustFinalValueCalculation(self,peerID,serviceID,startDate,stopDate):
        
        trustFinalValue = 0.5
        confDir, t ,tt = self.directTrustCalculation(peerID, serviceID, startDate, stopDate)
        #print "trust mana ",confDir, t ,tt
        gamaConfDir    = (self.getGama()*confDir)
        betaReputation = (self.getBeta()*self.reputationCalculation(peerID, serviceID, startDate, stopDate))
        trustFinalValue = (gamaConfDir+betaReputation) 
        hoje = datetime.today()
        period =  hoje.strftime('%d/%m/%Y %H:%M')
        
        ## rever
        self.getTrustFinal().addElement(TrustFinal(peerID,serviceID,serviceID,AbstractTrust.TRUSTF,trustFinalValue,period,True))      
        
        return trustFinalValue
    
    
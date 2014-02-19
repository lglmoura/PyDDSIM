'''
Created on 24/04/2010

@author: Luiz Gustavo
'''

from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.peer.trading.abstract_trading import AbstractTrading
from pydssim.peer.service.shared_period import SharePeriod
from pydssim.util.log.trading_logger import TradingLogger
from pydssim.peer.history.history import History
import traceback

class InformationServiceAgent(object):
    '''
    classdocs
    '''


    def __init__(self,tradingManager):
        '''
        Constructor
        '''
        
        self.__tradingManager = tradingManager
    
    def getTradingManager(self):
        return self.__tradingManager
    
    def verifyTrading(self,data):
        
        TradingLogger().resgiterLoggingInfo("Verify Trading ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingMetric,tradingQuantity,equivalenceEquivalenceResource, equivalenceEquivalenceUUID,sharePeriodMetric,equivalenceQuantityTrand,tradingDPeriodStart,tradingTPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd,sharePeriodDPeriodStart,sharePeriodTPeriodStart,sharePeriodDPeriodEnd,sharePeriodTPeriodEnd,tradingAttempt = data.split()
        
         
        # Put in History 
        
        history = History(peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingMetric,tradingQuantity,equivalenceEquivalenceResource,equivalenceEquivalenceUUID,sharePeriodMetric,equivalenceQuantityTrand,tradingDPeriodStart,tradingTPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd)
        
        self.getTradingManager().getPeer().getHistoryResource().addElement(history)
        
        
        service = None
        
        for service in self.getTradingManager().getPeer().getServices().getElements().values():
            
            if tradingServiceResource == service.getResource():
                break
        
        
             
        if not service:
           
            return False
        
        tradingPeriodStart = "%s %s"%(tradingDPeriodStart,tradingTPeriodStart)
        tradingPeriodEnd = "%s %s"%(tradingDPeriodEnd,tradingTPeriodEnd)
        
         
        # verify if service shared
        hasShare = service.hasSharePeriodswithQuantity(tradingPeriodStart,tradingPeriodEnd,tradingQuantity,tradingMetric)
        
       
       
        if not hasShare:
            
            return False
        
        #verificar quantidade 
        
        equivalenceRepository = self.getTradingManager().getPeer().getEquivalenceRepository()
        
        serviceEquivalent  = equivalenceRepository.getElementID(service.getUUID())
        
        hasEquiv = serviceEquivalent.hasEquivalencesForTag(equivalenceEquivalenceResource,tradingPeriodStart,tradingPeriodEnd)
        #print " Isa has equiv", hasEquiv
            
        if not hasEquiv:
            #print "+++++++++++++ isa false 3"
            return False
        
        trust = self.getTradingManager().getPeer().getTrustManager().TrustFinalValueCalculation(peerSource,
                                                                                                tradingServiceResource,
                                                                                                tradingPeriodStart,
                                                                                                tradingPeriodEnd) 
        
        
        equivalenceID,equivalence = hasEquiv.popitem()
        
        trading = self.getTradingManager().creatTradingService(service,tradingPeriodStart,tradingPeriodEnd,tradingQuantity,AbstractTrading.SERVER)
        trading.setUUID(tradingUUID)
        
        trading.setQuantityEquivalence(equivalenceQuantityTrand)
        trading.setEquivalence(equivalence)
        trading.addPeerTrading(peerSource,trust)
        
        self.getTradingManager().getTradings().addElement(trading)
        
        
        return True        
               
        

    
    def sendTradingForChildren(self,data):
        
        TradingLogger().resgiterLoggingInfo("send Tradind For Children ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        peerNeighbors = self.getTradingManager().getPeer().getPeerNeighbors()
        
       
        try:
            #print " neigSP",peerNeighbors.values()
            for host, port in peerNeighbors.values():
                 
                 
                #print "enter", host,port,self.getTradingManager().getPeer().getPID()           
                resp = self.getTradingManager().getPeer().connectAndSend(host, int(port), AbstractMessageHandler.TRADINGCH,data)#[0]
                #print "resp sendTradingForChildren",resp
                
                
                
        except:
            traceback.print_exc()
              
        
        return True     
        
    def sendTradingForSuperPeerNeighbor(self,superPeerNeig,level,data):
        
        TradingLogger().resgiterLoggingInfo("send Tradind For Super Peer Neighbor ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
       
        peerNeighbors = self.getTradingManager().getPeer().getSuperPeerNeighbor()
        
                
        #print "send super ----->>>>>--->>>>>>>>>>>-------------->>>> ",superPeerNeig,peerNeighbors
        
        for super,levelSP in peerNeighbors.iteritems():
            
            if super == superPeerNeig or levelSP >int(level)  :
                continue
            
            #print "Super - - - - -  > > >",super, self.getTradingManager().getPeer().getPID(),self.getTradingManager().getPeer().getLevelNeighbor()
            host, port = super.split(":")
      
            datasp = self.getTradingManager().getPeer().getPID()+" "+str(levelSP)+"~"+data
                       
            resp = self.getTradingManager().getPeer().connectAndSend(host, int(port), AbstractMessageHandler.TRADINGSN,datasp)#[0]
            
            
            
            
        return True    
            
    def __consultEquivalenceAndShare(self,service,periodStart,periodEnd):
        
        TradingLogger().resgiterLoggingInfo("consult Equivalence And Share ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        sharePeriods = {}
        flag = True 
        equivalence = None
        
        serviceEquivalences = self.getTradingManager().getPeer().getEquivalenceRepository()
        
        serviceEquivalence = serviceEquivalences.getElementID(service.getUUID())
        
        #equivalencesInPeriod = serviceEquivalence.getAllEquivalenceInPeriod(periodStart,periodEnd)
        
        equivalencesInPeriod = serviceEquivalence.getEquivalences()
        
        if not equivalencesInPeriod:
            return (equivalence,sharePeriods)
        
               
        for equivalenceID, equivalence in equivalencesInPeriod.iteritems():
            
            equivalenceService = equivalence.getEquivalence()
            #sharePeriods = equivalenceService.getResourceS().hasSharePeriods(periodStart,periodEnd)
            sharePeriods = equivalenceService.getResourceS().getSharePeriod()
            
            
            if  sharePeriods:
                flag = False
                break
                
        if flag:
            #Pensar em criar uma opcao qduo nao tiver equivalaencia
            pass
            
        return (equivalence,sharePeriods)    
    
    def searchServiceForTrading(self,trading):
        
        if trading.getType() == AbstractTrading.SERVER:
            #print "Server"
            return False
           
       
        TradingLogger().resgiterLoggingInfo("search Service For Trading ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        #if trading.getAttempt == 1:
        equivalence,sharePeriodsEquiva = self.__consultEquivalenceAndShare(trading.getService(), trading.getPeriodStart(), trading.getPeriodEnd())
        
        if not equivalence:
           
            return False
        
        quantityTrand = int((trading.getQuantity()*equivalence.getEquivalenceQuantity())/equivalence.getServiceQuantity())
        
        trading.setQuantityEquivalence(quantityTrand)
        trading.setEquivalence(equivalence)
        
        self.getTradingManager().getTradings().addElement(trading)
        
        sharePeriod  = None
        for shareID, sharePeriod in sharePeriodsEquiva.iteritems():
            if sharePeriod.getQuantity()>= quantityTrand and sharePeriod.getMetric() == trading.getMetric() and sharePeriod.getStatus() == SharePeriod.IDLE:
                sharePeriod.setStatus(SharePeriod.TRADING)
                break
                
        if not sharePeriod:
            return False
        
        
        
        superPeer = self.getTradingManager().getPeer().getMySuperPeer()
        #print "SuperPerr", superPeer,trading.getAttempt()
        peerSource      = self.getTradingManager().getPeer().getPID()
        
        TradingLogger().resgiterLoggingInfo("Send for SuperPeer = %s ,Peer = %s"%(superPeer,self.getTradingManager().getPeer().getPID()))
        
        hostSuper,portSuper = superPeer.split(":")
        try:
            
            msgSend = "%s %s %s %s %s %d %s %s %s %d %s %s %s %s %d"%(peerSource,trading.getUUID(),trading.getService().getResource(),trading.getService().getUUID(),trading.getMetric(),trading.getQuantity(),
                                              equivalence.getEquivalence().getResource(),equivalence.getEquivalence().getUUID(),sharePeriod.getMetric(),quantityTrand,trading.getPeriodStart(),
                                              trading.getPeriodEnd(),sharePeriod.getPeriodStart(),sharePeriod.getPeriodEnd(),trading.getAttempt())
               
            #print msgSend   
                         
            resp = self.getTradingManager().getPeer().connectAndSend(hostSuper, portSuper, AbstractMessageHandler.TRADINGSP,msgSend)#[0]
            #print "resp", resp
  
        except:
           traceback.print_exc()        
        
        return True
            
    def sendStartTrading(self,data):
        
        TradingLogger().resgiterLoggingInfo("**** Send Start Trading ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
      
        
        peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingMetric,tradingQuantity,equivalenceEquivalenceResource, equivalenceEquivalenceUUID,sharePeriodMetric,equivalenceQuantityTrand,tradingDPeriodStart,tradingTPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd,sharePeriodDPeriodStart,sharePeriodTPeriodStart,sharePeriodDPeriodEnd,sharePeriodTPeriodEnd,tradingAttempt = data.split()
        
        if peerSource == self.getTradingManager().getPeer().getPID():
            return False
         
        
       
        host,port = peerSource.split(":")
       
        
        msg = "%s %s"%(self.getTradingManager().getPeer().getPID(),tradingUUID)
                    
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGST,msg)#[0]
      
        
        peer,tradingUUID,responseTrand = resp[0][1].split()
        try:
            trading = self.__tradingManager.getTradings().getElementID(tradingUUID)
            trading.setStatus(responseTrand)
            self.__tradingManager.getTradings().addElement(trading)
            #print "resp sst",resp
           
        except:
                      
            traceback.print_exc()  
        
        
        return True
        
            
    def verifyTrust(self,data):
        
        TradingLogger().resgiterLoggingInfo("verify Trust ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        peer,tradingUUID = data.split()
        
        trading = self.__tradingManager.getTradings().getElementID(tradingUUID)
        
        
        if trading.getStatus() == AbstractTrading.STARTED:
               
            trust = self.getTradingManager().getPeer().getTrustManager().TrustFinalValueCalculation(peer,
                                                                                                    trading.getService().getTag(),
                                                                                                    trading.getPeriodStart(),
                                                                                                    trading.getPeriodEnd()) 
            trading.addPeerTrading(peer,trust)
           
        return "%s %s"%(data,trading.getStatus())    
            
        
    def sendResponseToPeerWinner(self,trading,myPeer,peer):
        
        print "Send sendResponseToPeerWinner ", self.getTradingManager().getPeer().getPID(),peer
        TradingLogger().resgiterLoggingInfo("** send Response To Peer Winner ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        msg = "%s %s %s"%(trading.getUUID(),AbstractTrading.COMPLETE,myPeer)
            
        host,port = peer.split(":")
                    
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGCP,msg)#[0]
  
         
        
        return resp[0][1]  
    
    
                
    def sendOwnershipCertificate(self,trading,myPeer,peer):
        
        
        
        TradingLogger().resgiterLoggingInfo("Send OwnershipCertificate ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        msg = "%s %s"%(trading.getUUID(),myPeer)
        
        print "Send  sendOwnershipCertificate ", self.getTradingManager().getPeer().getPID(), msg,peer
            
        host,port = peer.split(":")
                     
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGOC,msg)#[0]
       
        tradingUUID,ownershipCertificate = resp[0][1].split()
        
        #trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        #trading.setOwnershipCertificate(ownershipCertificate)
  
         
        
        return ownershipCertificate    
                    
    def recvOwner(self, data):
        
        TradingLogger().resgiterLoggingInfo("recv Owner ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        print "recv  OC", data
        
        tradingUUID,ownershipCertificate = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        trading.setOwnershipCertificate(ownershipCertificate)
        
        msg = "%s %s"%(trading.getUUID(),self.getTradingManager().getPeer().getURN())
        
        return msg  
        
        
        
    def sendResponseToPeerAll(self,trading,myPeer,peer):
        
        #print "SendAll", self.getTradingManager().getPeer().getPID()
        
        TradingLogger().resgiterLoggingInfo("Send Response To Peer All ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        for peerTrading in trading.getPeersTrading().keys():
                       
            if peerTrading == peer:
                continue
            
            msg = "%s %s %s"%(trading.getUUID(),AbstractTrading.NOTCOMLETE,myPeer)
                
            host,port = peerTrading.split(":")
                         
            resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGCP,msg)#[0]
      
             
    def recvResponseToPeer(self,data):
        
        TradingLogger().resgiterLoggingInfo("Recv Response To Peer ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        tradingUUID,status,myPeer = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        
        #colocar uma verificacao#
        
        
        msg = AbstractTrading.NOTCOMLETE
        if status == AbstractTrading.COMPLETE:
            trading.setStatus(status)
            msg = AbstractTrading.ACK
            
        return msg       
                  
            
    def recvResponseToPeerComplete(self,data):
        
        print "------------>>>>>>>> Complete ", self.getTradingManager().getPeer().getPID()
        
        TradingLogger().resgiterLoggingInfo("** Recv Response To Peer Complete ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        tradingUUID,status,myPeer = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        
        trading.setStatus(status)
        msg = AbstractTrading.NULL
        if status == AbstractTrading.COMPLETE:
            msg = AbstractTrading.ACK
            
        return msg
"""
Defines the module with the implementation AbstractPeer class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.peer.abstract_peer import AbstractPeer
from pydssim.util.decorator.public import createURN
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.super_peer_logger import SuperPeerLogger
import traceback

class SuperPeer(AbstractPeer):
    """
    Implements the basic functions of a peer.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self, urn=createURN("peer"),serverPort=4000, maxNeighbor=1):
        
        self.__superPeerNeighbors = {}
        self.__levelNeighbor = 1
        
        AbstractPeer.initialize(self, urn,serverPort, maxNeighbor, peerType = AbstractPeer.SUPER)
        
   
    def getSuperPeerNeighbor(self):
        return self.__superPeerNeighbors
    
    def insertSuperPeer(self,peerID,pid,level):
        
        dhost,dport = peerID.split(":")
        resp = self.connectAndSend(dhost, dport, AbstractMessageHandler.INSERTSPEER, 
                    '%s %d' % (pid,
                               int(level)))#[0]
        SuperPeerLogger().resgiterLoggingInfo ("Insert SuperPeers (%s,%s)" % (self.getServerHost(),self.getServerPort()))
        
    def updateLeveSuperPeer(self,portalID,peerID,level):
        
        dhost,dport = peerID.split(":")
        
        resp = self.connectAndSend(dhost, dport, AbstractMessageHandler.UPDATEPEERLEVEL, 
                    '%s %d' % (portalID,level))#[0]
        SuperPeerLogger().resgiterLoggingInfo ("Update %s in level %d" % (peerID,level))       
    
    def connectPortal(self, portalID, hops=1):
    
        """ ConnectPeers(host, port, hops) 
    
        Attempt to build the local peer list up to the limit stored by
        self.maxPeers, using a simple depth-first search given an
        initial host and port as starting point. The depth of the
        search is limited by the hops parameter.
    
        """
        
    
        peerID = None
        
        host,port = portalID.split(":")
    
        SuperPeerLogger().resgiterLoggingInfo ("Connecting to PortalPeers (%s,%s)" % (host,port))
        
        try:
            #print "contacting " #+ peerID
            _, peerID = self.connectAndSend(host, port, AbstractMessageHandler.PEERNAME, '')[0]
    
            
           
            self.insertSuperPeer(portalID,self.getPID(),self.getLevelNeighbor())
             
            # do recursive depth first search to add more peers
            resp = self.connectAndSend(host, port, AbstractMessageHandler.LISTSPEERS, '',
                        pid=peerID)
            
            
            
            if len(resp) > 1:
                resp.reverse()
            resp.pop()    # get rid of header count reply
            
            peers = {}
            while len(resp):
                nextpid,level,dportal = resp.pop()[1].split()
                peers[nextpid] = int(level)
               
                
            self.discoverNewNeighbor(peers, portalID, dportal)    
                
        except:
            traceback.print_exc()
            #print "eerrroooo" 
            self.removePeer(peerID)     
    
    def addSuperPeer(self,id,level):
        self.addSuperPeerNeighbor(id, level)
        
    
    def addSuperPeerNeighbor(self,id,level=1):
        
        if not (id in self.getSuperPeerNeighbor().keys()):
            SuperPeerLogger().resgiterLoggingInfo('Add SuperPeer %s in level : %s' % (id, self.getPID()))
            self.getSuperPeerNeighbor()[id]= int(level)
            
    def setLevelNeighbor(self,level):
        
        while self.__hasLevelNeighbor(level):
            level+=1 
        
        self.__levelNeighbor = level
        
    def __hasLevelNeighbor(self,level):
        
      
        return (level in self.getSuperPeerNeighbor().values())
       
    def __hasPeerNeighbor(self,peer):
        
        return (peer in self.getSuperPeerNeighbor().keys())  
        
     
    
    def getSuperPeerWithLevel(self,peers,level):
       
        return dict([(peerID,pLevel) for peerID, pLevel in peers.iteritems() if (pLevel == level and peerID != self.getPID())])
    
 
    def getLevelNeighbor(self):
        return self.__levelNeighbor
    
    def DisconectSuperPeer(self):
        pass
    
    def discoverNewNeighbor(self,peers,portalID,dportal):
         
        auxLevel = int(self.getLevelNeighbor())
        dportal = int(dportal)
         
        #print "---->>>>>  dportal, auxLevel",dportal,auxLevel,self.getPID()
        while dportal >= auxLevel:
            
            peerLevel =  self.getSuperPeerWithLevel(peers, auxLevel)
        
            
            if (not peerLevel):
               auxLevel+=1
               continue 
            
            if (peerLevel) and (self.__hasLevelNeighbor(auxLevel)):
               auxLevel+=1
               continue 
             
            peerID,level = peerLevel.popitem()
            
            if (self.__hasPeerNeighbor(peerID)):
               auxLevel+=1
               continue
            
            self.addSuperPeerNeighbor(peerID, level)
            
            self.insertSuperPeer(peerID,self.getPID(),level)
            
            if self.getLevelNeighbor() == level:
               self.setLevelNeighbor(self.getLevelNeighbor()+1)
               self.insertSuperPeer(portalID,self.getPID(),self.getLevelNeighbor())
                       
            self.updateLeveSuperPeer(portalID,peerID, level+1)
            #self.insertSuperPeer(portalID,peerID,level+1)
            
            
        
    

        
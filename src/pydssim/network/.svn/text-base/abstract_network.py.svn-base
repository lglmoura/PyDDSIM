
from sets import ImmutableSet
from multiprocessing import Semaphore
from pydssim.util.log.network_logger import NetworkLogger
from random import randint




class AbstractNetwork():
    """
    Defines the operations of Network .

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """
 
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, simulation, numberPeers , newPeerTime, maxNeighbors,portal="127.0.0.1",startPort=3999):
        
        self.__simulation = simulation
        
        self.__portalID = portal+":%s"%startPort
        
        self.__startPort = startPort
        
        self.__connectedPeers = {}
        self.__advertisedPeers = []
        self.__layout = {} 
        self.__peers = numberPeers
        self.__newPeerTime = newPeerTime
        self.__maxNeighbors = maxNeighbors
        #self.__looger = NetworkLogger()
        #self.__looger.resgiterLoggingInfo("Initialize Network => peers = %d , New Peer Time = %d, neighbors/peer = %d "%(numberPeers,newPeerTime,maxNeighbors))
        NetworkLogger().resgiterLoggingInfo("Initialize Network => peers = %d , New Peer Time = %d, neighbors/peer = %d gggggg"%(numberPeers,newPeerTime,maxNeighbors))
    
    
    def getSimulation(self):
        return self.__simulation
    
    def getPortalID(self):
        return self.__portalID
    
    def setPortalID(self, portalID):
        self.__portalID = portalID
    
    def setSimulation(self, simulation):
        self.__simulation = simulation
        return self.__simulation
    
    
    def getPeers(self):
        return self.__peers
    
    
    def getNewPeerTime(self):
        return self.__newPeerTime
    
    
    def getLayout(self):
        return self.__layout
    
    
    def setLayout(self, layout):
        self.__layout = layout
        return self.__layout
    
    
    def countPeers(self):
        semaphore = Semaphore()
        semaphore.acquire()
        tamPeers = len(self.__layout)
        semaphore.release()
        return tamPeers
   
    
    def addPeer(self, peer):
        
        if self.__layout.has_key(peer.getPID()):
            return False
        
        semaphore = Semaphore()
        semaphore.acquire()
        
        self.__layout[peer.getPID()] = peer
        semaphore.release()
        NetworkLogger().resgiterLoggingInfo("Add peer %s in Layout Network "%(peer.getPID()))
        return self.__layout.has_key(peer.getPID())

    
    def removePeer(self, peer):
        
        flag = True
        
        if not self.__layout.has_key(peer.getPID()):
            return False
        
        semaphore = Semaphore()
        semaphore.acquire()
        
        '''
        pode travar  pois estou chamando um sema dentro do outro?
        '''
        
        
        del self.__layout[peer.getPID()]
       
        
        flag = not self.__layout.has_key(peer.getPID())
        semaphore.release()
        
        return flag

   
    def getMaxNeighbor(self):
        return self.__maxNeighbors
         
    
    def getPeerID(self, peerId):
        
        semaphore = Semaphore()
        semaphore.acquire()
        peer = self.__layout[peerId]
        semaphore.release()
        return peer
    
    def getRandonPeer(self):
       
        return self.getPeerID(self.__layout.keys()[randint(0,self.countPeers()-1)])
    
    def getPeersFromLayout(self,peer):
       
        return dict([(peerID,peerN) for (peerID,peerN) in self.getLayout().iteritems() if (peerN.getPID() != peer.getPID())])
    
       
    
    

    
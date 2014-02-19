"""
Defines the module with the implementation AbstractPeer class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.peer.abstract_peer import AbstractPeer
from pydssim.util.decorator.public import public,createURN
from pydssim.util.log.portal_logger import PortalLogger
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from random import randint
import math

class PortalPeer(AbstractPeer):
    """
    Implements the basic functions of a peer.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self, urn=createURN("peer"),serverPort=4000, maxNeighbor=1):
        
        AbstractPeer.initialize(self,  urn,serverPort,maxNeighbor,peerType = AbstractPeer.PORTAL)
        
        
        self.__superPeers = {}
        
        self.__dimension = 1
    
    def getSuperPeers(self):
        return self.__superPeers
    
        
    def numberOfSuperPeers( self ):
   
        """ Return the number of known peer's. """
        return len(self.getSuperPeers()) 
    
    def getSuperPeerIDs( self ):
    
        """ Return a list of all known peer id's. """
        return self.getSuperPeers().keys() 
    
    
    def getDimension(self):
        return self.__dimension
    
    def updatePeerLevel(self,peerId,peerLevel): 
        self.__superPeers[peerId]=peerLevel
           
                   
           
    def addSuperPeer(self,peerId,peerLevel=1):
        self.__superPeers[peerId]=peerLevel
        PortalLogger().resgiterLoggingInfo('Add Super Peer %s in level : %s' % (peerId, peerLevel))
        ###
        #fazer o al do hyper
        
        if math.log(len(self.__superPeers),2) > self.__dimension:
            self.__dimension = int(math.log(len(self.__superPeers),2))+1
        
                
        #print self.__superPeers, self.__dimension
          
    
    def getSuperPeerWithLevel(self,level):
        superPeers = {}
        try:
            superPeers = dict([(pID,pLevel) for pID, pLevel in self.getSuperPeers().iteritems() if pLevel == level])
        except:
            pass    
        return superPeers
    
    def getSuperPeerWithLevelMin(self):
        superPeers = {}
        
        try:
            mini = min(self.getSuperPeers().values())
            superPeers = dict([(pID,pLevel) for pID, pLevel in self.getSuperPeers().iteritems() if pLevel == mini])
        except:
            pass    
        return superPeers
    
    

        
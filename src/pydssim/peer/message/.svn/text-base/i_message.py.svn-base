"""
Defines the module with Imessage class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""
class IMessage(object):
     
    ADVERTISEMENT = 0
    QUERY = 1
    SERVICE = 2
    SYSTEM = 3
    
    def __init__(self):
        raise NotImplementedError()
    
    def getSource(self):
        """
        Gets the identifier of source peer.
       
        """
        raise NotImplementedError()
    
    def getTarget(self):
        """
        Gets the identifier of target peer.
       
        """
        raise NotImplementedError()
    
    def getTTL(self):
        """
        Gets the time to live of message.
        
        """
        raise NotImplementedError()
    
    def getHop(self):
        """
        Gets the number of hops.
        
        """
        raise NotImplementedError()
    
    def setHop(self, hop):
        """
        Gets the number of hops.
        @param hop: number of hops
        
        """
        raise NotImplementedError()
    
    def clone(self):
        """
        Create a copy of peer-to-peer message.
        
        """
        raise NotImplementedError()
    
    def getHandle(self):
        """
        Gets the handle of peer-to-peer message.
      
        """
        raise NotImplementedError()
    
    def getId(self):
        """
        Gets the identifier of peer-to-peer message.
       
        """
        raise NotImplementedError()
    
    def getPriority(self):
        """
        Gets the priority of peer-to-peer message.
        
        """
        raise NotImplementedError()
    
    def init(self, id, source, target, ttl, priority):
        """
        Initializes peer-to-peer messages.
        @param id: the identifier of  message
        
        @param source: source  of message
       
        @param targetId: target  of  message
       
        @param ttl: time-to-live of  message
       
        @param priority: priority of  message
        
        """
        raise NotImplementedError()
    
    def getType(self):
        """
        Gets the type of message.
       
        """
        raise NotImplementedError()
    
    def registerPeer(self, peerId):
        raise NotImplementedError()
    
    def unregisterPeer(self, peerId):
        raise NotImplementedError()
    
    def countPeer(self):
        raise NotImplementedError()
    
    def hasPeer(self, peerId):
        raise NotImplementedError()
    
    def getPeer(self):
        raise NotImplementedError()
    
    def getFirst(self):
        raise NotImplementedError()
    
    def getLast(self):
        raise NotImplemented()
    
    def registerParameter(self, name, value):
        raise NotImplementedError()
    
    def getParameter(self, name):
        raise NotImplementedError()
    
    def unregisterParameter(self, name):
        raise NotImplementedError()
    
    def countParameters(self):
        raise NotImplementedError()
    
    def getParameterNames(self):
        raise NotImplementedError()
    
    def getParameterValues(self):
        raise NotImplementedError()
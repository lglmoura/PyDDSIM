from pydssim.util.interface import Interface
from pydssim.util.decorator.public import public

class INetwork(object):
    
    __metaclass__ = Interface
    
    def __init__(self):
        raise NotImplementedError()
    
       
    def getSimulation(self):
        raise NotImplementedError()
    
    def setSimulation(self, simInstance):
        raise NotImplementedError()
    
    def countPeers(self):
        raise NotImplementedError()
    
    def addPeer(self, peer):
        raise NotImplementedError()
    
    def removePeer(self, id):
        raise NotImplementedError()
    
    def getNeighbors(self, id):
        raise NotImplementedError()
    
    @public
    def getGraph(self):
        raise NotImplementedError()
    
    @public
    def addNode(self, id):
        raise NotImplementedError()
    
    @public
    def removeNode(self, id):
        raise NotImplementedError()
   
    
    @public
    def countNodes(self):
        raise NotImplementedError()
    
    @public
    def countConnections(self):
        raise NotImplementedError()
    
    @public
    def dispatchMessage(self, message):
        raise NotImplementedError()
    
    @public
    def isNeighbor(self, sourceId, targetId):
        raise NotImplementedError()
    
    @public
    def getPeer(self, id):
        raise NotImplementedError()
    
    def createConnection(self, sourceId, targetId):
        raise NotImplementedError()
    
    def removeConnection(self, sourceId, targetId):
        raise NotImplementedError()
    
    def increaseNumberOfConnectedPeers(self, peerId):
        raise NotImplementedError()
    
    def decreaseNumberOfConnectedPeers(self, peerId):
        raise NotImplementedError()
    
    def getPeerForConnection(self):
        raise NotImplementedError()
    
    def getPeerForDisconnection(self):
        raise NotImplementedError()
    
    def countConnectedPeers(self):
        raise NotImplementedError()
    
    def countDisconnectedPeers(self):
        raise NotImplementedError()
    
    def getPeerForAdvertisement(self):
        raise NotImplementedError()
    
    def registerPeerForAdvertisement(self, id):
        raise NotImplementedError()
    
    def unregisterPeerForAdvertisement(self, id):
        raise NotImplementedError()
    
    def getConnectedPeers(self):
        raise NotImplementedError()
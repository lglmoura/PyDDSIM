
class ITopology(object):
   
    """
    Defines the operations of Network topology.

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self):
        raise NotImplementedError()
    
    def addNeighbors(self, source, target):
        """
        Creates a connection between two peers.
        @param sourceId: the identifier of source peer
        @type sourceId: int
        @param targetId: the identifier of target peer
        @type targetId: int
        @return: If connection was created, returns True. Else, returns False.
        @rtype: bool
        """
        raise NotImplementedError()
    
    def removeNeighbor(self, source, target):
        """
        Removes a connection between two peers.
        @param sourceId: the identifier of source peer
        @type sourceId: int
        @param targetId: the identifier of target peer
        @type targetId: int
        @return: If connection was removed, returns True. Else, returns False.
        @rtype: bool
        """
        raise NotImplementedError()
    
    def getNeighbor(self, source, target):
        """
        Gets a Neighbor.
        @param sourceId: the identifier of source node
        @type sourceId: int
        @param targetId: the identifier of target node
        @type targetId: int
        @return: an INeighbor
        @rtype: INeighbor
        """
        raise NotImplementedError()
    
    def getNeighbors(self, peerId):
        """
        Gets the list of Neighbors in node
        @param nodeId: the identifier of node
        @type nodeId: int
        @return: a list
        @rtype: list
        """
        raise NotImplementedError()
    
    def countNeighbors(self, peerId):
        """
        Counts the number of Neighbors in node
        @param nodeId: the identifier of node
        @type nodeId: int
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def setNetwork(self, network):
        """
        Sets the peer-to-peer network.
        @param peerToPeerNetwork: an IPeerToPeerNetwork
        @type peerToPeerNetwork: IPeerToPeerNetwork
        @return: an IPeerToPeerNetwork
        @rtype: IPeerToPeerNetwork
        """
        raise NotImplementedError()
    
    def getNetwork(self):
        """
        Gets the peer-to-peer network.
        @return: an IPeerToPeerNetwork
        @rtype: IPeerToPeerNetwork
        """
        raise NotImplementedError()
    
    def getPeer(self, peerId):
        """
        Gets a Peer in topology.
        @param PeerId: the Peer identifier
        @type PeerId: int
        @return: a Peer
        @rtype: Peer
        """
        raise NotImplementedError()
    
    def getPeers(self):
        """
        Gets the list of Peer
        @return: a list
        @rtype: list
        """
        raise NotImplementedError()
    
    def countPeers(self):
        """
        Counts the number of Peers.
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def getNeighbors(self, peerId):
        """
        Gets the neighbors of peer
        @return: a list
        @rtype: list
        """
        raise NotImplementedError()
    
    def hasPeer(self, peerId):
        raise NotImplementedError()
    
   
'''
Created on 21/08/2009

@author: LGustavo
'''


class IRouterTable(object):
    """ Interface for Routing Table
    
    Classes inheriting from this should provide a suitable routing table for
    a parent Peer object (i.e. the local entity in the Kademlia network)
    """
    def __init__(self, parentPeerID):
        """
        @param parentPeerID: The 160-bit peer ID of the peer to which this
                             routing table belongs
        @type parentPeerID: str
        """
    def addNeighbor(self, neighbor):
        """ Add the given neighbor to the correct k-bucket; if it already
        exists, its status will be updated

        @param neighbor: The neighbor to add to this peer's k-buckets
        @type neighbor: kademlia.neighbor.Neighbor
        """
    
    def distance(self, keyOne, keyTwo):
        """ Calculate the XOR result between two string variables
        
        @return: XOR result of two long variables
        @rtype: long
        """
        

    def findClosePeers(self, key, count, _rpcPeerID=None):
        """ Finds a number of known peers closest to the peer/value with the
        specified key.
        
        @param key: the 160-bit key (i.e. the peer or value ID) to search for
        @type key: str
        @param count: the amount of neighbors to return
        @type count: int
        @param _rpcPeerID: Used during RPC, this is be the sender's Peer ID
                           Whatever ID is passed in the paramater will get
                           excluded from the list of returned neighbors.
        @type _rpcPeerID: str
        
        @return: A list of peer neighbors (C{kademlia.neighbor.Neighbor instances})
                 closest to the specified key. 
                 This method will return C{k} (or C{count}, if specified)
                 neighbors if at all possible; it will only return fewer if the
                 peer is returning all of the neighbors that it knows of.
        @rtype: list
        """
    def getNeighbor(self, neighborID):
        """ Returns the (known) neighbor with the specified peer ID
        
        @raise ValueError: No neighbor with the specified neighbor ID is known
                           by this peer
        """
    def getRefreshList(self, startIndex=0, force=False):
        """ Finds all k-buckets that need refreshing, starting at the
        k-bucket with the specified index, and returns IDs to be searched for
        in order to refresh those k-buckets

        @param startIndex: The index of the bucket to start refreshing at;
                           this bucket and those further away from it will
                           be refreshed. For example, when joining the
                           network, this peer will set this to the index of
                           the bucket after the one containing it's closest
                           neighbour.
        @type startIndex: index
        @param force: If this is C{True}, all buckets (in the specified range)
                      will be refreshed, regardless of the time they were last
                      accessed.
        @type force: bool
        
        @return: A list of peer ID's that the parent peer should search for
                 in order to refresh the routing Table
        @rtype: list
        """
    def removeNeighbor(self, neighborID):
        """ Remove the neighbor with the specified peer ID from the routing
        table
        
        @param neighborID: The peer ID of the neighbor to remove
        @type neighborID: str
        """
    def touchKBucket(self, key):
        """ Update the "last accessed" timestamp of the k-bucket which covers
        the range containing the specified key in the key/ID space
        
        @param key: A key in the range of the target k-bucket
        @type key: str
        """

'''
Created on 21/08/2009

@author: LGustavo
'''
import time, random

import constant_variable
from pydssim.network.protocol.dht.kademlia.k_bucket import KBucket
from pydssim.network.protocol.dht.kademlia.bucketFull import BucketFull
from pydssim.network.protocol.dht.kademlia.time_error_protocol import TimeoutErrorProtocol
from pydssim.network.protocol.dht.kademlia.i_router_table import IRouterTable

class AbstractRouterTable(IRouterTable):
    """ This class implements a routing table used by a Peer class.
    
    The Kademlia routing table is a binary tree whose leaves are k-buckets,
    where each k-bucket contains peers with some common prefix of their IDs.
    This prefix is the k-bucket's position in the binary tree; it therefore
    covers some range of ID values, and together all of the k-buckets cover
    the entire 160-bit ID (or key) space (with no overlap).
    
    @note: In this implementation, peers in the tree (the k-buckets) are
    added dynamically, as needed; this technique is described in the 13-page
    version of the Kademlia paper, in section 2.4. It does, however, use the
    C{PING} RPC-based k-bucket eviction algorithm described in section 2.2 of
    that paper.
    """
    def __init__(self, parentPeerID):
        """
        @param parentPeerID: The 160-bit peer ID of the peer to which this
                             routing table belongs
        @type parentPeerID: str
        """
        # Create the initial (single) k-bucket covering the range of the entire 160-bit ID space
        self._buckets = [KBucket(rangeMin=0, rangeMax=2**160)]
        
        self._parentPeerID = parentPeerID

    def addNeighbor(self, neighbor):
        """ Add the given neighbor to the correct k-bucket; if it already
        exists, its status will be updated

        @param neighbor: The neighbor to add to this peer's k-buckets
        @type neighbor: kademlia.neighbor.Neighbor
        """
        if neighbor.id == self._parentPeerID:
            return

        bucketIndex = self._kbucketIndex(neighbor.id)
        try:
            self._buckets[bucketIndex].addNeighbor(neighbor)
        except BucketFull:
            # The bucket is full; see if it can be split (by checking if its range includes the host peer's id)
            if self._buckets[bucketIndex].keyInRange(self._parentPeerID):
                self._splitBucket(bucketIndex)
                # Retry the insertion attempt
                self.addNeighbor(neighbor)
            else:
                         
                headNeighbor = self._buckets[bucketIndex]._neighbors[0]
    
                def replaceNeighbor(failure):
                    """ Callback for the deferred PING RPC to see if the head
                    peer in the k-bucket is still responding
                    
                    @type failure: twisted.python.failure.Failure
                    """
                    failure.trap(TimeoutErrorProtocol)
                    print '==replacing neighbor=='
                    # Remove the old neighbor...
                    deadNeighborID = failure.getErrorMessage()
                    try:
                        self._buckets[bucketIndex].removeNeighbor(deadNeighborID)
                    except ValueError:
                        # The neighbor has already been removed (probably due to a timeout)
                        pass
                    # ...and add the new one at the tail of the bucket
                    self.addNeighbor(neighbor)
                
                # Ping the least-recently seen neighbor in this k-bucket
                headNeighbor = self._buckets[bucketIndex]._neighbors[0]
                df = headNeighbor.ping()
                # If there's an error (i.e. timeout), remove the head neighbor, and append the new one
                df.addErrback(replaceNeighbor)
             
    def distance(self, keyOne, keyTwo):
        """ Calculate the XOR result between two string variables
        
        @return: XOR result of two long variables
        @rtype: long
        """
        valKeyOne = long(keyOne.encode('hex'), 16)
        valKeyTwo = long(keyTwo.encode('hex'), 16)
        return valKeyOne ^ valKeyTwo         
                
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
        #if key == self.id:
        #    bucketIndex = 0 #TODO: maybe not allow this to continue?
        #else:
        bucketIndex = self._kbucketIndex(key)
        closestPeers = self._buckets[bucketIndex].getNeighbors(constant_variable.k, _rpcPeerID)
        # This method must return k neighbors (even if we have the peer with the specified key as peer ID), 
        # unless there is less than k remote peers in the routing table
        i = 1
        canGoLower = bucketIndex-i >= 0
        canGoHigher = bucketIndex+i < len(self._buckets)
        # Fill up the peer list to k peers, starting with the closest neighbouring peers known 
        while len(closestPeers) < constant_variable.k and (canGoLower or canGoHigher):
            #TODO: this may need to be optimized
            if canGoLower:
                closestPeers.extend(self._buckets[bucketIndex-i].getNeighbors(constant_variable.k - len(closestPeers), _rpcPeerID))
                canGoLower = bucketIndex-(i+1) >= 0
            if canGoHigher:
                closestPeers.extend(self._buckets[bucketIndex+i].getNeighbors(constant_variable.k - len(closestPeers), _rpcPeerID))
                canGoHigher = bucketIndex+(i+1) < len(self._buckets)
            i += 1
        return closestPeers

    def getNeighbor(self, neighborID):
        """ Returns the (known) neighbor with the specified peer ID
        
        @raise ValueError: No neighbor with the specified neighbor ID is known
                           by this peer
        """
        bucketIndex = self._kbucketIndex(neighborID)
        try:
            neighbor = self._buckets[bucketIndex].getNeighbor(neighborID)
        except ValueError:
            raise
        else:
            return neighbor

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
        bucketIndex = startIndex
        refreshIDs = []
        for bucket in self._buckets[startIndex:]:
            if force or (int(time.time()) - bucket.lastAccessed >= constant_variable.refreshTimeout):
                searchID = self._randomIDInBucketRange(bucketIndex)
                refreshIDs.append(searchID)
            bucketIndex += 1
        return refreshIDs

    def removeNeighbor(self, neighborID):
        """ Remove the neighbor with the specified peer ID from the routing
        table
        
        @param neighborID: The peer ID of the neighbor to remove
        @type neighborID: str
        """
        bucketIndex = self._kbucketIndex(neighborID)
        try:
            self._buckets[bucketIndex].removeNeighbor(neighborID)
        except ValueError:
            #print 'removeNeighbor(): Neighbor not in routing table'
            return

    def touchKBucket(self, key):
        """ Update the "last accessed" timestamp of the k-bucket which covers
        the range containing the specified key in the key/ID space
        
        @param key: A key in the range of the target k-bucket
        @type key: str
        """
        bucketIndex = self._kbucketIndex(key)
        self._buckets[bucketIndex].lastAccessed = int(time.time())

    def _kbucketIndex(self, key):
        """ Calculate the index of the k-bucket which is responsible for the
        specified key (or ID)
        
        @param key: The key for which to find the appropriate k-bucket index
        @type key: str
        
        @return: The index of the k-bucket responsible for the specified key
        @rtype: int
        """
        valKey = long(key.encode('hex'), 16)
        i = 0
        for bucket in self._buckets:
            if bucket.keyInRange(valKey):
                return i
            else:
                i += 1
        return i

    def _randomIDInBucketRange(self, bucketIndex):
        """ Returns a random ID in the specified k-bucket's range
        
        @param bucketIndex: The index of the k-bucket to use
        @type bucketIndex: int
        """
        idValue = random.randrange(self._buckets[bucketIndex].rangeMin, self._buckets[bucketIndex].rangeMax)
        randomID = hex(idValue)[2:]
        if randomID[-1] == 'L':
            randomID = randomID[:-1]
        if len(randomID) % 2 != 0:
            randomID = '0' + randomID
        randomID = randomID.decode('hex')
        randomID = (20 - len(randomID))*'\x00' + randomID
        return randomID

    def _splitBucket(self, oldBucketIndex):
        """ Splits the specified k-bucket into two new buckets which together
        cover the same range in the key/ID space
        
        @param oldBucketIndex: The index of k-bucket to split (in this table's
                               list of k-buckets)
        @type oldBucketIndex: int
        """
        # Resize the range of the current (old) k-bucket
        oldBucket = self._buckets[oldBucketIndex]
        splitPoint = oldBucket.rangeMax - (oldBucket.rangeMax - oldBucket.rangeMin)/2
        # Create a new k-bucket to cover the range split off from the old bucket
        newBucket = KBucket(splitPoint, oldBucket.rangeMax)
        oldBucket.rangeMax = splitPoint
        # Now, add the new bucket into the routing table tree
        self._buckets.insert(oldBucketIndex + 1, newBucket)
        # Finally, copy all nodes that belong to the new k-bucket into it...
        for neighbor in oldBucket._neighbors:
            if newBucket.keyInRange(neighbor.id):
                newBucket.addNeighbor(neighbor)
        # ...and remove them from the old bucket
        for neighbor in newBucket._neighbors:
            oldBucket.removeNeighbor(neighbor)
'''
Created on 21/12/2009

@author: LGustavo
'''
from pydssim.network.protocol.dht.kademlia.abstract_router_table import AbstractRouterTable
 
class DefaultRouterTable(AbstractRouterTable):
    """ A version of the "tree"-type routing table specified by Kademlia,
    along with contact accounting optimizations specified in section 4.1 of
    of the 13-page version of the Kademlia paper.
    """
    def __init__(self, parentPeerID):
        AbstractRouterTable.__init__(self, parentPeerID)
        # Cache containing peers eligible to replace stale k-bucket entries
        self._replacementCache = {}
        
    def addPeer(self, peer):
        """ Add the given peer to the correct k-bucket; if it already
        exists, its status will be updated

        @param peer: The peer to add to this peer's k-buckets
        @type peer: kademlia.peer.Peer
        """
        if peer.id == self._parentPeerID:
            return

        # Initialize/reset the "successively failed RPC" counter
        peer.failedRPCs = 0

        bucketIndex = self._kbucketIndex(peer.id)
        try:
            self._buckets[bucketIndex].addPeer(peer)
        except BucketFull:
            # The bucket is full; see if it can be split (by checking if its range includes the host peer's id)
            if self._buckets[bucketIndex].keyInRange(self._parentPeerID):
                self._splitBucket(bucketIndex)
                # Retry the insertion attempt
                self.addPeer(peer)
            else:
                # We can't split the k-bucket
                # NOTE: This implementation follows section 4.1 of the 13 page version
                # of the Kademlia paper (optimized peer accounting without PINGs
                #- results in much less network traffic, at the expense of some memory)

                # Put the new peer in our replacement cache for the corresponding k-bucket (or update it's position if it exists already)
                if not self._replacementCache.has_key(bucketIndex):
                    self._replacementCache[bucketIndex] = []
                if peer in self._replacementCache[bucketIndex]:
                    self._replacementCache[bucketIndex].remove(peer)
                #TODO: Using k to limit the size of the peer replacement cache - maybe define a seperate value for this in constants.py?
                elif len(self._replacementCache) >= constants.k:
                    self._replacementCache.pop(0)
                self._replacementCache[bucketIndex].append(peer)
    
    def removePeer(self, peerID):
        """ Remove the peer with the specified peer ID from the routing
        table
        
        @param peerID: The peer ID of the peer to remove
        @type peerID: str
        """
        bucketIndex = self._kbucketIndex(peerID)
        try:
            peer = self._buckets[bucketIndex].getPeer(peerID)
        except ValueError:
            #print 'removePeer(): Peer not in routing table'
            return
        peer.failedRPCs += 1
        if peer.failedRPCs >= 5:        
            self._buckets[bucketIndex].removePeer(peerID)
            # Replace this stale peer with one from our replacemnent cache, if we have any
            if self._replacementCache.has_key(bucketIndex):
                if len(self._replacementCache[bucketIndex]) > 0:
                    self._buckets[bucketIndex].addContact( self._replacementCache[bucketIndex].pop() )

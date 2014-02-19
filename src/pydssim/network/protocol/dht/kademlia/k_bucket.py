'''
Created on 20/07/2009

@author: LGustavo
'''

import constant_variable
from bucketFull import BucketFull

class KBucket(object):
    """ Description - later
    """
    def __init__(self, rangeMin, rangeMax):
        """
        @param rangeMin: The lower boundary for the range in the 160-bit ID
                         space covered by this k-bucket
        @param rangeMax: The upper boundary for the range in the ID space
                         covered by this k-bucket
        """
        self.lastAccessed = 0
        self.rangeMin = rangeMin
        self.rangeMax = rangeMax
        self._neighbors = list()

    def addNeighbor(self, neighbor):
        """ Add neighbor to _neighbor list in the right order. This will move the
        neighbor to the end of the k-bucket if it is already present.
        
        @raise kademlia.kbucket.BucketFull: Raised when the bucket is full and
                                            the neighbor isn't in the bucket
                                            already
        
        @param neighbor: The neighbor to add
        @type neighbor: kademlia.neighbor.Neighbor
        """
        if neighbor in self._neighbors:
            # Move the existing neighbor to the end of the list
            # - using the new neighbor to allow add-on data (e.g. optimization-specific stuff) to pe updated as well
            self._neighbors.remove(neighbor)
            self._neighbors.append(neighbor)
        elif len(self._neighbors) < constant_variable.k:
            self._neighbors.append(neighbor)
        else:
            raise BucketFull("No space in bucket to insert neighbor")

    def getNeighbor(self, neighborID):
        """ Get the neighbor specified node ID"""
        index = self._neighbors.index(neighborID)
        return self._neighbors[index]

    def getNeighbors(self, count=-1, excludeNeighbor=None):
        """ Returns a list containing up to the first count number of neighbors
        
        @param count: The amount of neighbors to return (if 0 or less, return
                      all neighbors)
        @type count: int
        @param excludeNeighbor: A neighbor to exclude; if this neighbor is in
                               the list of returned values, it will be
                               discarded before returning. If a C{str} is
                               passed as this argument, it must be the
                               neighbor's ID. 
        @type excludeNeighbor: kademlia.neighbor.Neighbor or str
        
        
        @raise IndexError: If the number of requested neighbors is too large
        
        @return: Return up to the first count number of neighbors in a list
                If no neighbors are present an empty is returned
        @rtype: list
        """
        # Return all neighbors in bucket
        if count <= 0:
            count = len(self._neighbors)

        # Get current neighbor number
        currentLen = len(self._neighbors)

        # If count greater than k - return only k neighbors
        if count > constant_variable.k:
            count = constant_variable.k

        # Check if count value in range and,
        # if count number of neighbors are available
        if not currentLen:
            neighborList = list()

        # length of list less than requested amount
        elif currentLen < count:
            neighborList = self._neighbors[0:currentLen]
        # enough neighbors in list
        else:
            neighborList = self._neighbors[0:count]
            
        if excludeNeighbor in neighborList:
            neighborList.remove(excludeNeighbor)

        return neighborList

    def removeNeighbor(self, neighbor):
        """ Remove given neighbor from list
        
        @param neighbor: The neighbor to remove, or a string containing the
                        neighbor's node ID
        @type neighbor: kademlia.neighbor.Neighbor or str
        
        @raise ValueError: The specified neighbor is not in this bucket
        """
        self._neighbors.remove(neighbor)
    
    def keyInRange(self, key):
        """ Tests whether the specified key (i.e. node ID) is in the range
        of the 160-bit ID space covered by this k-bucket (in otherwords, it
        returns whether or not the specified key should be placed in this
        k-bucket)
        
        @param key: The key to test
        @type key: str or int
        
        @return: C{True} if the key is in this k-bucket's range, or C{False}
                 if not.
        @rtype: bool
        """
        if isinstance(key, str):
            key = long(key.encode('hex'), 16)
        return self.rangeMin <= key < self.rangeMax

    def __len__(self):
        return len(self._neighbors)

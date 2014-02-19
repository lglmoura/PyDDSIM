'''
Created on 19/07/2009

@author: LGustavo
'''

import hashlib, random, time

from twisted.internet import defer

import constant_variable
import abstract_router_table
from pydssim.network.protocol.dht.kademlia.default_router_table import DefaultRouterTable
import pydssim.network.protocol.dht.kademlia.datastore.i_datastore

from pydssim.network.protocol.dht.kademlia.kademlia_protocol import KademliaProtocol 
from pydssim.network.protocol.dht.kademlia.time_error_protocol import TimeoutErrorProtocol 
import twisted.internet.reactor
import twisted.internet.threads
from neighbor import Neighbor
from datastore.dict_datastore import DictDataStore
from datastore.sqllite_datastore import SQLLiteDataStore


def rpcmethod(func):
    """ Decorator to expose Peer methods as remote procedure calls
    
    Apply this decorator to methods in the Peer class (or a subclass) in order
    to make them remotely callable via the DHT's RPC mechanism.
    """
    func.rpcmethod = True
    return func

class Peer(object):
    """ Local peer in the Kademlia network
    
    This class represents a single local peer in a Kademlia network; in other
    words, this class encapsulates an Entangled-using application's "presence"
    in a Kademlia network.
    
    all interactions with the Kademlia network by a client
    application is performed via this class (or a subclass). 
    """
    def __init__(self, id=None, udpPort=4000, dataStore=None, routerTableClass=None, networkProtocol=None):
        """
        @param dataStore: The data store to use. This must be class inheriting
                          from the C{DataStore} interface (or providing the
                          same API). How the data store manages its data
                          internally is up to the implementation of that data
                          store.
        @type dataStore: dht.kademlia.datastore.DataStore
        @param routerTable: The router table class to use. Since there exists
                             some ambiguity as to how the router table should be
                             implemented in Kademlia, a different router table
                             may be used, as long as the appropriate API is
                             exposed. This should be a class, not an object,
                             in order to allow the Peer to pass an
                             auto-generated peer ID to the routertable object
                             upon instantiation (if necessary). 
        @type routerTable: dht.kademlia.routertable.RoutingTable
        @param networkProtocol: The network protocol to use. This can be
                                overridden from the default to (for example)
                                change the format of the physical RPC messages
                                being transmitted.
        @type networkProtocol: dht.kademlia.protocol.KademliaProtocol
        """
        if id != None:
            self.id = id
        else:
            self.id = self._generateID()
        self.port = udpPort
        self._listeningPort = None # object implementing Twisted IListeningPort
        # This will contain a deferred created when joining the network, to enable publishing/retrieving information from
        # the DHT as soon as the peer is part of the network (add callbacks to this deferred if scheduling such operations
        # before the peer has finished joining the network)
        self._joinDeferred = None
        # Create k-buckets (for storing neighbors)
        #self._buckets = []
        #for i in range(160):
        #    self._buckets.append(kbucket.KBucket())
        if routerTableClass == None:
            self._routerTable = DefaultRouterTable(self.id)
        else:
            self._routerTable = routerTableClass(self.id)

        # Initialize this peer's network access mechanisms
        if networkProtocol == None:
            self._protocol = KademliaProtocol(self)
        else:
            self._protocol = networkProtocol
        # Initialize the data storage mechanism used by this peer
        if dataStore == None:
            #self._dataStore = datastore.DictDataStore()
            self._dataStore = DictDataStore()
        else:
            self._dataStore = dataStore
            # Try to restore the peer's state...
            if 'peerState' in self._dataStore:
                state = self._dataStore['peerState']
                self.id = state['id']
                for neighborTriple in state['closestPeers']:
                    neighbor = Neighbor(neighborTriple[0], neighborTriple[1], neighborTriple[2], self._protocol)
                    self._routerTable.addNeighbor(neighbor)
        
        
    def __del__(self):
        self._persistState()
        self._listeningPort.stopListening()
        
    def getID(self):
        return self.id

    def joinNetwork(self, knownPeerAddresses=None):
        """ Causes the Peer to join the Kademlia network; normally, this
        should be called before any other DHT operations.
        
        @param knownPeerAddresses: A sequence of tuples containing IP address
                                   information for existing peers on the
                                   Kademlia network, in the format:
                                   C{(<ip address>, (udp port>)}
        @type knownPeerAddresses: tuple
        """
        # Prepare the underlying Kademlia protocol
       
        self._listeningPort = twisted.internet.reactor.listenUDP(self.port, self._protocol)
        # Create temporary neighbor information for the list of addresses of known peers
       
        if knownPeerAddresses != None:
            bootstrapNeighbors = []
            for address, port in knownPeerAddresses:
               
                neighbor = Neighbor(self._generateID(), address, port, self._protocol)
                
                bootstrapNeighbors.append(neighbor)
        else:
            bootstrapNeighbors = None
        # Initiate the Kademlia joining sequence - perform a search for this peer's own ID
        print "Short List", bootstrapNeighbors
        self._joinDeferred = self._iterativeFind(self.id, bootstrapNeighbors)

        self._joinDeferred.addCallback(self._persistState)
        # Start refreshing k-buckets periodically, if necessary
        twisted.internet.reactor.callLater(constant_variable.checkRefreshInterval, self._refreshPeer) 

    def printNeighbors(self):
        print '\n\nNODE CONTACTS\n==============='
        for i in range(len(self._routerTable._buckets)):
           
            for neighbor in self._routerTable._buckets[i]._neighbors:
                print neighbor
        print '=================================='
      

    def iterativeStore(self, key, value, originalPublisherID=None, age=0):
        """ The Kademlia store operation
        
        Call this to store/republish data in the DHT.
        
        @param key: The hashtable key of the data
        @type key: str
        @param value: The actual data (the value associated with C{key})
        @type value: str
        @param originalPublisherID: The peer ID of the peer that is the
                                    B{original} publisher of the data
        @type originalPublisherID: str
        @param age: The relative age of the data (time in seconds since it was
                    originally published). Note that the original publish time
                    isn't actually given, to compensate for clock skew between
                    different peers.
        @type age: int
        """
        #print '      iterativeStore called'
        if originalPublisherID == None:
            originalPublisherID = self.id
        # Prepare a callback for doing "STORE" RPC calls
        def executeStoreRPCs(peers):
            #print '        .....execStoreRPCs called'
            if len(peers) >= constant_variable.k:
                # If this peer itself is closer to the key than the last (furthest) peer in the list,
                # we should store the value at ourselves as well
                if self._routerTable.distance(key, self.id) < self._routerTable.distance(key, peers[-1].id):
                    peers.pop()
                    self.store(key, value, originalPublisherID=originalPublisherID, age=age)
            else:
                self.store(key, value, originalPublisherID=originalPublisherID, age=age)
            for neighbor in peers:
                neighbor.store(key, value, originalPublisherID, age)
            return peers
        # Find k peers closest to the key...
        df = self.iterativeFindPeer(key)
        # ...and send them STORE RPCs as soon as they've been found
        df.addCallback(executeStoreRPCs)
        return df

    def iterativeFindPeer(self, key):
        """ The basic Kademlia peer lookup operation
        
        Call this to find a remote peer in the P2P overlay network.
        
        @param key: the 160-bit key (i.e. the peer or value ID) to search for
        @type key: str
        
        @return: This immediately returns a deferred object, which will return
                 a list of k "closest" neighbors (C{kademlia.neighbor.Neighbor}
                 objects) to the specified key as soon as the operation is
                 finished.
        @rtype: twisted.internet.defer.Deferred
        """
        return self._iterativeFind(key)

    def iterativeFindValue(self, key):
        """ The Kademlia search operation (deterministic)
        
        Call this to retrieve data from the DHT.
        
        @param key: the 160-bit key (i.e. the value ID) to search for
        @type key: str
        
        @return: This immediately returns a deferred object, which will return
                 either one of two things:
                     - If the value was found, it will return a Python
                     dictionary containing the searched-for key (the C{key}
                     parameter passed to this method), and its associated
                     value, in the format:
                     C{<str>key: <str>data_value}
                     - If the value was not found, it will return a list of k
                     "closest" neighbors (C{kademlia.neighbor.Neighbor} objects)
                     to the specified key
        @rtype: twisted.internet.defer.Deferred
        """
        # Prepare a callback for this operation
        outerDf = defer.Deferred()
        def checkResult(result):
            if type(result) == dict:
                # We have found the value; now see who was the closest neighbor without it...
                if 'closestPeerNoValue' in result:
                    # ...and store the key/value pair
                    neighbor = result['closestPeerNoValue']
                    neighbor.store(key, result[key])
                outerDf.callback(result)
            else:
                # The value wasn't found, but a list of neighbors was returned
                # Now, see if we have the value (it might seem wasteful to search on the network
                # first, but it ensures that all values are properly propagated through the
                # network
                if key in self._dataStore:
                    # Ok, we have the value locally, so use that
                    value = self._dataStore[key]
                    # Send this value to the closest peer without it
                    if len(result) > 0:
                        neighbor = result[0]
                        neighbor.store(key, value)
                    outerDf.callback({key: value})
                else:
                    # Ok, value does not exist in DHT at all
                    outerDf.callback(result)

        # Execute the search
        df = self._iterativeFind(key, rpc='findValue')
        df.addCallback(checkResult)
        return outerDf

    def addNeighbor(self, neighbor):
        """ Add/update the given neighbor; simple wrapper for the same method
        in this object's RoutingTable object

        @param neighbor: The neighbor to add to this peer's k-buckets
        @type neighbor: kademlia.neighbor.Neighbor
        """
        self._routerTable.addNeighbor(neighbor)

    def removeNeighbor(self, neighborID):
        """ Remove the neighbor with the specified peer ID from this peer's
        table of known peers. This is a simple wrapper for the same method
        in this object's RoutingTable object
        
        @param neighborID: The peer ID of the neighbor to remove
        @type neighborID: str
        """
        self._routerTable.removeNeighbor(neighborID)

    def findNeighbor(self, neighborID):
        """ Find a dht.kademlia.neighbor.Neighbor object for the specified
        cotact ID
        
        @param neighborID: The neighbor ID of the required Neighbor object
        @type neighborID: str
                 
        @return: Neighbor object of remote peer with the specified peer ID,
                 or None if the neighbor was not found
        @rtype: twisted.internet.defer.Deferred
        """
        try:
            neighbor = self._routerTable.getNeighbor(neighborID)
            df = defer.Deferred()
            df.callback(neighbor)
        except ValueError:
            def parseResults(peers):
                if neighborID in peers:
                    neighbor = peers[peers.index(neighborID)]
                    return neighbor
                else:
                    return None
            df = self.iterativeFindPeer(neighborID)
            df.addCallback(parseResults)
        return df

    @rpcmethod
    def ping(self):
        """ Used to verify neighbor between two Kademlia peers
        
        @rtype: str
        """
        return 'pong'

    @rpcmethod
    def store(self, key, value, originalPublisherID=None, age=0, **kwargs):
        """ Store the received data in this peer's local hash table
        
        @param key: The hashtable key of the data
        @type key: str
        @param value: The actual data (the value associated with C{key})
        @type value: str
        @param originalPublisherID: The peer ID of the peer that is the
                                    B{original} publisher of the data
        @type originalPublisherID: str
        @param age: The relative age of the data (time in seconds since it was
                    originally published). Note that the original publish time
                    isn't actually given, to compensate for clock skew between
                    different peers.
        @type age: int

        @rtype: str
        
        @todo: Since the data (value) may be large, passing it around as a buffer
               (which is the case currently) might not be a good idea... will have
               to fix this (perhaps use a stream from the Protocol class?)
        """
        # Get the sender's ID (if any)
        if '_rpcPeerID' in kwargs:
            rpcSenderID = kwargs['_rpcPeerID']
        else:
            rpcSenderID = None

        if originalPublisherID == None:
            if rpcSenderID != None:
                originalPublisherID = rpcSenderID
            else:
                raise TypeError, 'No publisher specifed, and RPC caller ID not available. Data requires an original publisher.'

        now = int(time.time())
        originallyPublished = now - age
        self._dataStore.setItem(key, value, now, originallyPublished, originalPublisherID)
        return 'OK'

    @rpcmethod
    def findPeer(self, key, **kwargs):
        """ Finds a number of known peers closest to the peer/value with the
        specified key.
        
        @param key: the 160-bit key (i.e. the peer or value ID) to search for
        @type key: str

        @return: A list of neighbor triples closest to the specified key.
                 This method will return C{k} (or C{count}, if specified)
                 neighbors if at all possible; it will only return fewer if the
                 peer is returning all of the neighbors that it knows of.
        @rtype: list
        """
        # Get the sender's ID (if any)
        
        if '_rpcPeerID' in kwargs:
            rpcSenderID = kwargs['_rpcPeerID']
        else:
            rpcSenderID = None
        
        
        neighbors = self._routerTable.findClosePeers(key, constant_variable.k, rpcSenderID)
        neighborTriples = []
        for neighbor in neighbors:
            neighborTriples.append( (neighbor.id, neighbor.address, neighbor.port) )
        return neighborTriples

    @rpcmethod
    def findValue(self, key, **kwargs):
        """ Return the value associated with the specified key if present in
        this peer's data, otherwise execute FIND_NODE for the key
        
        @param key: The hashtable key of the data to return
        @type key: str
        
        @return: A dictionary containing the requested key/value pair,
                 or a list of neighbor triples closest to the requested key.
        @rtype: dict or list
        """
        if key in self._dataStore:
            return {key: self._dataStore[key]}
        else:
            
            return self.findPeer(key, **kwargs)

    def _generateID(self):
        """ Generates a 160-bit pseudo-random identifier
        
        @return: A globally unique 160-bit pseudo-random identifier
        @rtype: str
        """
        hash = hashlib.sha1()
        hash.update(str(random.getrandbits(255)))
        return hash.digest()

    def _iterativeFind(self, key, startupShortlist=None, rpc='findPeer'):
        """ The basic Kademlia iterative lookup operation (for peers/values)
        
        This builds a list of k "closest" neighbors through iterative use of
        the "FIND_NODE" RPC, or if C{findValue} is set to C{True}, using the
        "FIND_VALUE" RPC, in which case the value (if found) may be returned
        instead of a list of neighbors
        
        @param key: the 160-bit key (i.e. the peer or value ID) to search for
        @type key: str
        @param startupShortlist: A list of neighbors to use as the starting
                                 shortlist for this search; this is normally
                                 only used when the peer joins the network
        @type startupShortlist: list
        @param rpc: The name of the RPC to issue to remote peers during the
                    Kademlia lookup operation (e.g. this sets whether this
                    algorithm should search for a data value (if
                    rpc='findValue') or not. It can thus be used to perform
                    other operations that piggy-back on the basic Kademlia
                    lookup operation (Entangled's "delete" RPC, for instance).
        @type rpc: str
        
        @return: If C{findValue} is C{True}, the algorithm will stop as soon
                 as a data value for C{key} is found, and return a dictionary
                 containing the key and the found value. Otherwise, it will
                 return a list of the k closest peers to the specified key
        @rtype: twisted.internet.defer.Deferred
        """
        
        if rpc != 'findPeer':
            findValue = True
        else:
            findValue = False
        
        shortlist = []
        
        if startupShortlist == None:
            shortlist = self._routerTable.findClosePeers(key, constant_variable.alpha)
            if key != self.id:
                # Update the "last accessed" timestamp for the appropriate k-bucket
                self._routerTable.touchKBucket(key)
            if len(shortlist) == 0:
                # This peer doesn't know of any other peers
                fakeDf = defer.Deferred()
                fakeDf.callback([])
                return fakeDf
        else:
            # This is used during the bootstrap process; peer ID's are most probably fake
            shortlist = startupShortlist

        # List of active queries; len() indicates number of active probes
        # - using lists for these variables, because Python doesn't allow binding a new value to a name in an enclosing (non-global) scope
        activeProbes = []
        # List of neighbor IDs that have already been queried
        alreadyNeighbored = []
        # Probes that were active during the previous iteration
        # A list of found and known-to-be-active remote peers
        activeNeighbors = []
        # This should only contain one entry; the next scheduled iteration call
        pendingIterationCalls = []
        prevClosestPeer = [None]
        findValueResult = {}
        slowPeerCount = [0]

        def extendShortlist(responseTuple):
            """ @type responseMsg: kademlia.msgtypes.ResponseMessage """
            # The "raw response" tuple contains the response message, and the originating address info
            responseMsg = responseTuple[0]
            originAddress = responseTuple[1] # tuple: (ip adress, udp port)
            # Make sure the responding peer is valid, and abort the operation if it isn't
            if responseMsg.peerID in activeNeighbors or responseMsg.peerID == self.id:
                return responseMsg.peerID

            # Mark this peer as active
            if responseMsg.peerID in shortlist:
                # Get the neighbor information from the shortlist...
                aNeighbor = shortlist[shortlist.index(responseMsg.peerID)]
            else:
                # If it's not in the shortlist; we probably used a fake ID to reach it
                # - reconstruct the neighbor, using the real peer ID this time
                aNeighbor = Neighbor(responseMsg.peerID, originAddress[0], originAddress[1], self._protocol)
            activeNeighbors.append(aNeighbor)
            # This makes sure "bootstrap"-peers with "fake" IDs don't get queried twice
            if responseMsg.peerID not in alreadyNeighbored:
                alreadyNeighbored.append(responseMsg.peerID)
            # Now grow extend the (unverified) shortlist with the returned neighbors
            result = responseMsg.response
            #TODO: some validation on the result (for guarding against attacks)
            # If we are looking for a value, first see if this result is the value
            # we are looking for before treating it as a list of neighbor triples
            if findValue == True and type(result) == dict:
                # We have found the value
                findValueResult[key] = result[key]
            else:
                if findValue == True:
                    # We are looking for a value, and the remote peer didn't have it
                    # - mark it as the closest "empty" peer, if it is
                    if 'closestPeerNoValue' in findValueResult:
                        if self._routerTable.distance(key, responseMsg.peerID) < self._routerTable.distance(key, activeNeighbors[0].id):
                            findValueResult['closestPeerNoValue'] = aNeighbor
                    else:
                        findValueResult['closestPeerNoValue'] = aNeighbor
                for neighborTriple in result:
                    if isinstance(neighborTriple, (list, tuple)) and len(neighborTriple) == 3:
                        testNeighbor = Neighbor(neighborTriple[0], neighborTriple[1], neighborTriple[2], self._protocol)
                        if testNeighbor not in shortlist:
                            shortlist.append(testNeighbor)
            return responseMsg.peerID

        def removeFromShortlist(failure):
            """ @type failure: twisted.python.failure.Failure """
            failure.trap(TimeoutErrorProtocol)
            deadNeighborID = failure.getErrorMessage()
            if deadNeighborID in shortlist:
                shortlist.remove(deadNeighborID)
            return deadNeighborID

        def cancelActiveProbe(neighborID):
            activeProbes.pop()
            if len(activeProbes) <= constant_variable.alpha/2 and len(pendingIterationCalls):
                # Force the iteration
                pendingIterationCalls[0].cancel()
                del pendingIterationCalls[0]
                #print 'forcing iteration ================='
                searchIteration()

        # Send parallel, asynchronous FIND_NODE RPCs to the shortlist of neighbors
        def searchIteration():
            #print '==> searchiteration'
            slowPeerCount[0] = len(activeProbes)
            # Sort the discovered active peers from closest to furthest
            activeNeighbors.sort(lambda firstNeighbor, secondNeighbor, targetKey=key: cmp(self._routerTable.distance(firstNeighbor.id, targetKey), self._routerTable.distance(secondNeighbor.id, targetKey)))
            # This makes sure a returning probe doesn't force calling this function by mistake
            while len(pendingIterationCalls):
                del pendingIterationCalls[0]
            # See if should continue the search
            if key in findValueResult:
                #print '++++++++++++++ DONE (findValue found) +++++++++++++++\n\n'
                outerDf.callback(findValueResult)
                return
            elif len(activeNeighbors) and findValue == False:
                if (len(activeNeighbors) >= constant_variable.k) or (activeNeighbors[0] == prevClosestPeer[0] and len(activeProbes) == slowPeerCount[0]):
                    # TODO: Re-send the FIND_NODEs to all of the k closest peers not already queried
                    # Ok, we're done; either we have accumulated k active neighbors or no improvement in closestPeer has been noted
                    #if len(activeNeighbors) >= constants.k:
                    #    print '++++++++++++++ DONE (test for k active neighbors) +++++++++++++++\n\n'
                    #else:
                    #    print '++++++++++++++ DONE (test for closest peer) +++++++++++++++\n\n'
                    outerDf.callback(activeNeighbors)
                    return
            # The search continues...
            if len(activeNeighbors):
                prevClosestPeer[0] = activeNeighbors[0]
            neighboredNow = 0
            shortlist.sort(lambda firstNeighbor, secondNeighbor, targetKey=key: cmp(self._routerTable.distance(firstNeighbor.id, targetKey), self._routerTable.distance(secondNeighbor.id, targetKey)))
            # Store the current shortList length before neighboring other peers
            prevShortlistLength = len(shortlist)
            for neighbor in shortlist:
                if neighbor.id not in alreadyNeighbored:
                    activeProbes.append(neighbor.id)
                    rpcMethod = getattr(neighbor, rpc)
                    df = rpcMethod(key, rawResponse=True)
                    df.addCallback(extendShortlist)
                    df.addErrback(removeFromShortlist)
                    df.addCallback(cancelActiveProbe)
                    alreadyNeighbored.append(neighbor.id)
                    neighboredNow += 1
                if neighboredNow == constant_variable.alpha:
                    break
            if len(activeProbes) > slowPeerCount[0] \
                or (len(shortlist) < constant_variable.k and len(activeNeighbors) < len(shortlist) and len(activeProbes) > 0):
                #print '----------- scheduling next call -------------'
                # Schedule the next iteration if there are any active calls (Kademlia uses loose parallelism)
                call = twisted.internet.reactor.callLater(constant_variable.iterativeLookupDelay, searchIteration) #IGNORE:E1101
                pendingIterationCalls.append(call)
            # Check for a quick neighbor response that made an update to the shortList
            elif prevShortlistLength < len(shortlist):
                # Ensure that the closest neighbors are taken from the updated shortList
                searchIteration()
            else:
                #print '++++++++++++++ DONE (logically) +++++++++++++\n\n'
                # If no probes were sent, there will not be any improvement, so we're done
                outerDf.callback(activeNeighbors)

        outerDf = defer.Deferred()
        # Start the iterations
        searchIteration()
        return outerDf


    def _persistState(self, *args):
        state = {'id': self.id,
                 'closestPeers': self.findPeer(self.id)}
        now = int(time.time())
        self._dataStore.setItem('peerState', state, now, now, self.id)

    def _refreshPeer(self):
        """ Periodically called to perform k-bucket refreshes and data
        replication/republishing as necessary """
        #print 'refreshPeer called'
        df = self._refreshRoutingTable()
        df.addCallback(self._republishData)
        df.addCallback(self._scheduleNextPeerRefresh)

    def _refreshRoutingTable(self):
        peerIDs = self._routerTable.getRefreshList(0, False)
        outerDf = defer.Deferred()
        def searchForNextPeerID(dfResult=None):
            if len(peerIDs) > 0:
                searchID = peerIDs.pop()
                df = self.iterativeFindPeer(searchID)
                df.addCallback(searchForNextPeerID)
            else:
                # If this is reached, we have finished refreshing the router table
                outerDf.callback(None)
        # Start the refreshing cycle
        searchForNextPeerID()
        return outerDf

    def _republishData(self, *args):
        #print '---republishData() called'
        df = twisted.internet.threads.deferToThread(self._threadedRepublishData)
        return df

    def _scheduleNextPeerRefresh(self, *args):
        #print '==== sheduling next refresh'
        twisted.internet.reactor.callLater(constants.checkRefreshInterval, self._refreshPeer)

    def _threadedRepublishData(self, *args):
        """ Republishes and expires any stored data (i.e. stored
        C{(key, value pairs)} that need to be republished/expired
        
        This method should run in a deferred thread
        """
        #print '== republishData called, peer:',ord(self.id[0])
        expiredKeys = []
        for key in self._dataStore:
            # Filter internal variables stored in the datastore
            if key == 'peerState':
                continue
            now = int(time.time())
            originalPublisherID = self._dataStore.originalPublisherID(key)
            age = now - self._dataStore.originalPublishTime(key)
            #print '  peer:',ord(self.id[0]),'key:',ord(key[0]),'orig publishing time:',self._dataStore.originalPublishTime(key),'now:',now,'age:',age,'lastPublished age:',now - self._dataStore.lastPublished(key),'original pubID:', ord(originalPublisherID[0])
            if originalPublisherID == self.id:
                # This peer is the original publisher; it has to republish
                # the data before it expires (24 hours in basic Kademlia)
                if age >= constants.dataExpireTimeout:
                    #print '    REPUBLISHING key:', key
                    #self.iterativeStore(key, self._dataStore[key])
                    twisted.internet.reactor.callFromThread(self.iterativeStore, key, self._dataStore[key])
            else:
                # This peer needs to replicate the data at set intervals,
                # until it expires, without changing the metadata associated with it
                # First, check if the data has expired
                if age >= constants.dataExpireTimeout:
                    # This key/value pair has expired (and it has not been republished by the original publishing peer
                    # - remove it
                    expiredKeys.append(key)
                elif now - self._dataStore.lastPublished(key) >= constants.replicateInterval:
                    # ...data has not yet expired, and we need to replicate it
                    #print '    replicating key:', key,'age:',age
                    #self.iterativeStore(key=key, value=self._dataStore[key], originalPublisherID=originalPublisherID, age=age)
                    twisted.internet.reactor.callFromThread(self.iterativeStore, key=key, value=self._dataStore[key], originalPublisherID=originalPublisherID, age=age)
        for key in expiredKeys:
            #print '    expiring key:', key
            del self._dataStore[key]
        #print 'done with threadedDataRefresh()'


        
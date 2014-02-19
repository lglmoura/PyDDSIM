'''
Created on 21/07/2009

@author: LGustavo
'''

import time

from twisted.internet import protocol, defer
from twisted.python import failure
import twisted.internet.reactor

import constant_variable
from pydssim.network.protocol.dht.kademlia.bencode import Bencode
from pydssim.network.protocol.dht.kademlia.message.request_message import RequestMessage
from pydssim.network.protocol.dht.kademlia.message.response_message import ResponseMessage
from pydssim.network.protocol.dht.kademlia.message.error_message import ErrorMessage
from pydssim.network.protocol.dht.kademlia.message.default_message_translator import DefaultMessageTranslator
from pydssim.network.protocol.dht.kademlia.neighbor import Neighbor
from pydssim.network.protocol.dht.kademlia.time_error_protocol import TimeoutErrorProtocol

reactor = twisted.internet.reactor

class KademliaProtocol(protocol.DatagramProtocol):
    """ Implements all low-level network-related functions of a Kademlia peer """
    msgSizeLimit = constant_variable.udpDatagramMaxSize-26
    maxToSendDelay = 10**-3#0.05
    minToSendDelay = 10**-5#0.01

    def __init__(self, peer, msgEncoder=Bencode(), msgTranslator=DefaultMessageTranslator()):
        self._peer = peer
        self._encoder = msgEncoder
        self._translator = msgTranslator
        self._sentMessages = {}
        self._partialMessages = {}
        self._partialMessagesProgress = {}
        self._next = 0
        self._callLaterList = {}
        

    def sendRPC(self, neighbor, method, args, rawResponse=False):
        """ Sends an RPC to the specified neighbor

        @param neighbor: The neighbor (remote peer) to send the RPC to
        @type neighbor: kademlia.neighbors.Neighbor
        @param method: The name of remote method to invoke
        @type method: str
        @param args: A list of (non-keyword) arguments to pass to the remote
                    method, in the correct order
        @type args: tuple
        @param rawResponse: If this is set to C{True}, the caller of this RPC
                            will receive a tuple containing the actual response
                            message object and the originating address tuple as
                            a result; in other words, it will not be
                            interpreted by this class. Unless something special
                            needs to be done with the metadata associated with
                            the message, this should remain C{False}.
        @type rawResponse: bool

        @return: This immediately returns a deferred object, which will return
                 the result of the RPC call, or raise the relevant exception
                 if the remote peer raised one. If C{rawResponse} is set to
                 C{True}, however, it will always return the actual response
                 message (which may be a C{ResponseMessage} or an
                 C{ErrorMessage}).
        @rtype: twisted.internet.defer.Deferred
        """
        msg = RequestMessage(self._peer.id, method, args)
        msgPrimitive = self._translator.toPrimitive(msg)
        encodedMsg = self._encoder.encode(msgPrimitive)

        df = defer.Deferred()
        if rawResponse:
            df._rpcRawResponse = True

        # Set the RPC timeout timer
        timeoutCall = reactor.callLater(constant_variable.rpcTimeout, self._msgTimeout, msg.id) #IGNORE:E1101
        # Transmit the data
        self._send(encodedMsg, msg.id, (neighbor.address, neighbor.port))
        self._sentMessages[msg.id] = (neighbor.id, df, timeoutCall)
        return df

    def datagramReceived(self, datagram, address):
        """ Handles and parses incoming RPC messages (and responses)

        @note: This is automatically called by Twisted when the protocol
               receives a UDP datagram
        """
        if datagram[0] == '\x00' and datagram[25] == '\x00':
            totalPackets = (ord(datagram[1]) << 8) | ord(datagram[2])
            msgID = datagram[5:25]
            seqNumber = (ord(datagram[3]) << 8) | ord(datagram[4])
            if msgID not in self._partialMessages:
                self._partialMessages[msgID] = {}
            self._partialMessages[msgID][seqNumber] = datagram[26:]
            if len(self._partialMessages[msgID]) == totalPackets:
                keys = self._partialMessages[msgID].keys()
                keys.sort()
                data = ''
                for key in keys:
                    data += self._partialMessages[msgID][key]
                    datagram = data
                del self._partialMessages[msgID]
            else:
                return
        try:
            msgPrimitive = self._encoder.decode(datagram)
        except encoding.DecodeError:
            # We received some rubbish here
            return
        
        message = self._translator.fromPrimitive(msgPrimitive)
        remoteNeighbor = Neighbor(message.peerID, address[0], address[1], self)
        
        # Refresh the remote peer's details in the local peer's k-buckets
        self._peer.addNeighbor(remoteNeighbor)

        if isinstance(message, RequestMessage):
            # This is an RPC method request
            self._handleRPC(remoteNeighbor, message.id, message.request, message.args)
        elif isinstance(message, ResponseMessage):
            # Find the message that triggered this response
            if self._sentMessages.has_key(message.id):
                # Cancel timeout timer for this RPC
                df, timeoutCall = self._sentMessages[message.id][1:3]
                timeoutCall.cancel()
                del self._sentMessages[message.id]

                if hasattr(df, '_rpcRawResponse'):
                    # The RPC requested that the raw response message and originating address be returned; do not interpret it
                    df.callback((message, address))
                elif isinstance(message, ErrorMessage):
                    # The RPC request raised a remote exception; raise it locally
                    if message.exceptionType.startswith('exceptions.'):
                        exceptionClassName = message.exceptionType[11:]
                    else:
                        localModuleHierarchy = self.__module__.split('.')
                        remoteHierarchy = message.exceptionType.split('.')
                        #strip the remote hierarchy
                        while remoteHierarchy[0] == localModuleHierarchy[0]:
                            remoteHierarchy.pop(0)
                            localModuleHierarchy.pop(0)
                        exceptionClassName = '.'.join(remoteHierarchy)
                    remoteException = None
                    try:
                        exec 'remoteException = %s("%s")' % (exceptionClassName, message.response)
                    except Exception:
                        # We could not recreate the exception; create a generic one
                        remoteException = Exception(message.response)
                    df.errback(remoteException)
                else:
                    # We got a result from the RPC
                    df.callback(message.response)
            else:
                # If the original message isn't found, it must have timed out
                #TODO: we should probably do something with this...
                pass

    def _send(self, data, rpcID, address):
        """ Transmit the specified data over UDP, breaking it up into several
        packets if necessary
        
        
        """
        if len(data) > self.msgSizeLimit:
            # We have to spread the data over multiple UDP datagrams, and provide sequencing information
            # 1st byte is transmission type id, bytes 2 & 3 are the total number of packets in this transmission, bytes 4 & 5 are the sequence number for this specific packet
            totalPackets = len(data) / self.msgSizeLimit
            if len(data) % self.msgSizeLimit > 0:
                totalPackets += 1
            encTotalPackets = chr(totalPackets >> 8) + chr(totalPackets & 0xff)
            seqNumber = 0
            startPos = 0
            while seqNumber < totalPackets:
                #reactor.iterate() #IGNORE:E1101
                packetData = data[startPos:startPos+self.msgSizeLimit]
                encSeqNumber = chr(seqNumber >> 8) + chr(seqNumber & 0xff)
                txData = '\x00%s%s%s\x00%s' % (encTotalPackets, encSeqNumber, rpcID, packetData)
                self._sendNext(txData, address)

                startPos += self.msgSizeLimit
                seqNumber += 1
        else:
            self._sendNext(data, address)

    def _sendNext(self, txData, address):
        """ Send the next UDP packet """
        ts = time.time()
        delay = 0
        if ts >= self._next:
            delay = self.minToSendDelay
            self._next = ts + self.minToSendDelay
        else:
            delay = (self._next-ts) + self.maxToSendDelay
            self._next += self.maxToSendDelay
        if self.transport:
            laterCall = reactor.callLater(delay, self.transport.write, txData, address)
            for key in self._callLaterList.keys():
                if key <= ts:
                    del self._callLaterList[key]
            self._callLaterList[self._next] = laterCall

    def _sendResponse(self, neighbor, rpcID, response):
        """ Send a RPC response to the specified neighbor
        """
        msg = ResponseMessage(rpcID, self._peer.id, response)
        msgPrimitive = self._translator.toPrimitive(msg)
        encodedMsg = self._encoder.encode(msgPrimitive)
        self._send(encodedMsg, rpcID, (neighbor.address, neighbor.port))

    def _sendError(self, neighbor, rpcID, exceptionType, exceptionMessage):
        """ Send an RPC error message to the specified neighbor
        """
        msg = ErrorMessage(rpcID, self._peer.id, exceptionType, exceptionMessage)
        msgPrimitive = self._translator.toPrimitive(msg)
        encodedMsg = self._encoder.encode(msgPrimitive)
        self._send(encodedMsg, rpcID, (neighbor.address, neighbor.port))

    def _handleRPC(self, senderNeighbor, rpcID, method, args):
        """ Executes a local function in response to an RPC request """
        # Set up the deferred callchain
        def handleError(f):
            self._sendError(senderNeighbor, rpcID, f.type, f.getErrorMessage())

        def handleResult(result):
            self._sendResponse(senderNeighbor, rpcID, result)

        df = defer.Deferred()
        df.addCallback(handleResult)
        df.addErrback(handleError)

        # Execute the RPC
        func = getattr(self._peer, method, None)
        if callable(func) and hasattr(func, 'rpcmethod'):
            # Call the exposed Peer method and return the result to the deferred callback chain
            try:
                try:
                    # Try to pass the sender's peer id to the function...
                    result = func(*args, **{'_rpcPeerID': senderNeighbor.id, '_rpcPeerNeighbor': senderNeighbor})
                except TypeError:
                    # ...or simply call it if that fails
                    result = func(*args)
            except Exception, e:
                df.errback(failure.Failure(e))
            else:
                df.callback(result)
        else:
            # No such exposed method
            df.errback( failure.Failure( AttributeError('Invalid method: %s' % method) ) )

    def _msgTimeout(self, messageID):
        """ Called when an RPC request message times out """
        # Find the message that timed out
        if self._sentMessages.has_key(messageID):
            remoteNeighborID, df = self._sentMessages[messageID][0:2]
            if self._partialMessages.has_key(messageID):
                # We are still receiving this message
                # See if any progress has been made; if not, kill the message
                if self._partialMessagesProgress.has_key(messageID):
                    if len(self._partialMessagesProgress[messageID]) == len(self._partialMessages[messageID]):
                        # No progress has been made
                        del self._partialMessagesProgress[messageID]
                        del self._partialMessages[messageID]
                        df.errback(failure.Failure(TimeoutError(remoteNeighborID)))
                        return
                # Reset the RPC timeout timer
                timeoutCall = reactor.callLater(constants.rpcTimeout, self._msgTimeout, messageID) #IGNORE:E1101
                self._sentMessages[messageID] = (remoteNeighborID, df, timeoutCall)
                return
            del self._sentMessages[messageID]
            # The message's destination peer is now considered to be dead;
            # raise an (asynchronous) TimeoutError exception and update the host peer
            self._peer.removeNeighbor(remoteNeighborID)
            df.errback(failure.Failure(TimeoutErrorProtocol(remoteNeighborID)))
        else:
            # This should never be reached
            print "ERROR: deferred timed out, but is not present in sent messages list!"

    def stopProtocol(self):
        """ Called when the transport is disconnected.
        
        Will only be called once, after all ports are disconnected.
        """
        for key in self._callLaterList.keys():
            try:
                if key > time.time():
                    self._callLaterList[key].cancel()
            except Exception, e:
                print e
            del self._callLaterList[key]
            #TODO: test: do we really need the reactor.iterate() call?
            reactor.iterate()

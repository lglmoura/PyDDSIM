'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler

class MessageHandlerListPeer(AbstractMessageHandler):
    
    def __init__(self,peer ):
        self.initialize(peer,"LISTPEER",AbstractMessageHandler.LISTPEERS)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the LISTPEERS message type. Message data is not used. """

        self.getPeer().getPeerLock().acquire()
        try:
            #print 'Listing peers %d' % self.numberOfPeers()
            peerConn.sendData(AbstractMessageHandler.REPLY, '%d' % self.getPeer().numberOfPeers())
            for pid in self.getPeer().getPeerIDs():
                host,port,super = self.getPeer().getPeer(pid)
                
                peerConn.sendData(AbstractMessageHandler.REPLY, '%s %s %d %s' % (pid, host, port, super))
        finally:
            self.getPeer().getPeerLock().release()
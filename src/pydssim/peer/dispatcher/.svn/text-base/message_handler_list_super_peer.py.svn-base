'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.message_logger import MessageLogger
import traceback

class MessageHandlerListSuperPeer(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"LISTSPEERS",AbstractMessageHandler.LISTSPEERS)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the LISTSPEERS message type. Message data is not used. """

        self.getPeer().getPeerLock().acquire()
        try:
            try:
                
                if self.getPeer().numberOfSuperPeers() > 0:
                    dimension = self.getPeer().getDimension()
                    peerConn.sendData(AbstractMessageHandler.REPLY, '%d' % self.getPeer().numberOfSuperPeers())
                    for pid,level in self.getPeer().getSuperPeers().iteritems():
                        
                        peerConn.sendData(AbstractMessageHandler.REPLY, '%s %d %d' % (pid,int(level),dimension))
                else:
                    
                    peerConn.sendData(AbstractMessageHandler.FIRSTSP, '%d'%self.getPeer().numberOfSuperPeers())
                
                MessageLogger().resgiterLoggingInfo('List Super Peer %s: %s' % (str(peerConn), data))    
                        
            except:
                
                MessageLogger().resgiterLoggingInfo('invalid List Super Peer %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()        
        finally:
            self.getPeer().getPeerLock().release()
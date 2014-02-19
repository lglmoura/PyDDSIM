'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.message_logger import MessageLogger
import traceback

class MessageHandlerUpdatePeerLevel(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"UPDATEPEERLEVEL",AbstractMessageHandler.UPDATEPEERLEVEL)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the INSERTPEER (join) message type. The message data
        should be a string of the form, "peerid  host  port", where peer-id
        is the canonical name of the peer that desires to be added to this
        peer's list of peers, host and port are the necessary data to connect
        to the peer.
    
        """
        self.getPeer().getPeerLock().acquire()
        try:
            try:
                
                portalID,level = data.split()
                #print "UPpid, UPlevel",self.getPeer().getPID(),level
                self.getPeer().setLevelNeighbor(int(level))
                
                self.getPeer().insertSuperPeer(portalID,self.getPeer().getPID(),self.getPeer().getLevelNeighbor())
                
            except:
                
                MessageLogger().resgiterLoggingInfo('invalid update Peerleve %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()
        finally:
            self.getPeer().getPeerLock().release()
'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.message_logger import MessageLogger
import traceback

class MessageHandlerInsertSuperPeer(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"INSERTSPEER",AbstractMessageHandler.INSERTSPEER)
        
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
                
                peerID,level = data.split()
                
                             
                if peerID not in self.getPeer().getPeerIDs() and peerID != self.getPeer().getPID():
                    
                    self.getPeer().addSuperPeer(peerID,int(level))
                    
                    peerConn.sendData(AbstractMessageHandler.REPLY, 'Join: peer added: %s' % peerID)
                    
                    
                    
                else:
                   
                    peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: peer already inserted %s'
                               % peerID)
            except:
                
                MessageLogger().resgiterLoggingInfo('invalid insert %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()
        finally:
            self.getPeer().getPeerLock().release()
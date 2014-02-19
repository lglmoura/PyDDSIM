'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler


class MessageHandlerPeerExit(AbstractMessageHandler):
    
    def __init__(self,peer ):
        self.initialize(peer,"PEEREXIT",AbstractMessageHandler.PEEREXIT)
        
    def executeHandler(self,peerConn,data):
        
        self.getPeer().getPeerLock().acquire()
        try:
            
            peerID,host,port = data.split()
            if peerID in self.getPeer().getPeerIDs():
                msg = 'Quit: peer removed: %s' % peerID 
                #print msg
                peerConn.sendData(AbstractMessageHandler.REPLY, msg)
                self.getPeer().removePeer(peerID)
            else:
                msg = 'Quit: peer not found: %s' % peerID 
                #print msg
                peerConn.sendData(AbstractMessageHandler.ERROR, msg)
            #print msg    
        finally:
            self.getPeer().getPeerLock().release()
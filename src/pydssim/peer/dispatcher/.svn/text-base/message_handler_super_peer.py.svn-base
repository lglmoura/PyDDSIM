'''
Created on 23/01/2010

@author: LGustavo
'''

from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler


class MessageHandlerSuperPeer(AbstractMessageHandler):
    
    def __init__(self, peer):
        self.initialize(peer,"SUPERPEER",AbstractMessageHandler.SUPERPEER)
        
    def executeHandler(self,peerConn,data):
        
        self.getPeer().getPeerLock().acquire()
        try:
            try:
                
                super = data.split()
                 
                if self.getPeer().getMySuperPeer() == AbstractPeer.NULL:
                    self.getPeer().setMySuperPeer(super)                    
                    return
                
            except:
                Logger().resgiterLoggingInfo('invalid insert %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Super: incorrect arguments')
        finally:
            self.getPeer().getPeerLock().release()
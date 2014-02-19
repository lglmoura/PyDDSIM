'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.message_logger import MessageLogger
import traceback

class MessageHandlerTradingSuperforNeighbor(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"TRADINGSN",AbstractMessageHandler.TRADINGSN)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the TRUSTFINAL message type. Message data is not used. """

        self.getPeer().getPeerLock().acquire()
        try:
            try:
                
                superPeerNeig,data = data.split("~")
                superPeerNeig,level = superPeerNeig.split()
                #print "MessageHandlerTradingSuperforNeighbor Level-->-->--> ",superPeerNeig,level
                
                
                
                self.getPeer().getTradingManager().getISA().sendTradingForSuperPeerNeighbor(superPeerNeig,level,data) 
                
                self.getPeer().getTradingManager().getISA().sendTradingForChildren(data)
                
                   
                MessageLogger().resgiterLoggingInfo('TRADINGSN %s %s: %s' % (self.getPeer().getPID(),str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.REPLY, self.getPeer().getPID())
                
                       
            except:
                
                MessageLogger().resgiterLoggingInfo('invalid TurstFinalValue %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()        
        finally:
            
            self.getPeer().getPeerLock().release()
'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.message_logger import MessageLogger
import traceback

class MessageHandlerTradingComplete(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"TRADINGCP",AbstractMessageHandler.TRADINGCP)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the TRUSTFINAL message type. Message data is not used. """

        self.getPeer().getPeerLock().acquire()
        try:
            try:
                #print "data", data
                              
                msg = self.getPeer().getTradingManager().getISA().recvResponseToPeer(data)
                MessageLogger().resgiterLoggingInfo('TRADINGCP%s %s: %s' % (self.getPeer().getPID(),str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.REPLY, msg)
                
                       
            except:
                
                MessageLogger().resgiterLoggingInfo('invalid TurstFinalValue %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()        
        finally:
            self.getPeer().getPeerLock().release()
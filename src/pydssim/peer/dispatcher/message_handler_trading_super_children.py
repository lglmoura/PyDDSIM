'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.message_logger import MessageLogger
import traceback

class MessageHandlerTradingSuperforChildren(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"TRADINGCH",AbstractMessageHandler.TRADINGCH)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the TRUSTFINAL message type. Message data is not used. """

        self.getPeer().getPeerLock().acquire()
        try:
            try:
                
                MessageLogger().resgiterLoggingInfo('TRADINGSCH %s %s: %s' % (self.getPeer().getPID(),str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.REPLY, self.getPeer().getPID())              
                
                if self.getPeer().getTradingManager().getISA().verifyTrading(data):
                    #print "TCH",self.getPeer().getPID()
                    self.getPeer().getTradingManager().getISA().sendStartTrading(data)
                #else:
                #    print "NO TCH",self.getPeer().getPID()
               
                
                       
            except:
                
                MessageLogger().resgiterLoggingInfo('invalid TurstFinalValue %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()        
        finally:
            self.getPeer().getPeerLock().release()
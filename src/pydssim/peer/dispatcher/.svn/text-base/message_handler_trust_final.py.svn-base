'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.message_logger import MessageLogger
import traceback

class MessageHandlerTrustFinal(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"TRUSTFINAL",AbstractMessageHandler.TRUSTFINAL)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the TRUSTFINAL message type. Message data is not used. """

        self.getPeer().getPeerLock().acquire()
        try:
            try:
                #print "data", data
                
                peerID,service,startDate,startTime,stopDate,stopTime = data.split()
                
                startDate = "%s %s"%(startDate,startTime)
                stopDate = "%s %s"%(stopDate,stopTime)
               
                trustFinalValue = self.getPeer().getTrustManager().getTrustFinalValue(peerID,service,startDate,stopDate)
                MessageLogger().resgiterLoggingInfo('TrustFinalValue %s %s: %s %f' % (self.getPeer().getPID(),str(peerConn), data,trustFinalValue))
                peerConn.sendData(AbstractMessageHandler.REPLY, '%f' % trustFinalValue)
                
                       
            except:
                
                MessageLogger().resgiterLoggingInfo('invalid TurstFinalValue %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()        
        finally:
            self.getPeer().getPeerLock().release()
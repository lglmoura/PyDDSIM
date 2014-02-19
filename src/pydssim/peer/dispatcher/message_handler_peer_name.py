'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler

class MessageHandlerPeerName(AbstractMessageHandler):
    
    def __init__(self,peer ):
        self.initialize(peer,"PEERNAME",AbstractMessageHandler.PEERNAME)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the NAME message type. Message data is not used. """
        #print " peercom -------------->>>>>>>", peerConn.getHost(),peerConn.getPort(),peerConn.getSocket().getpeername()
        peerConn.sendData(AbstractMessageHandler.REPLY, self.getPeer().getPID())
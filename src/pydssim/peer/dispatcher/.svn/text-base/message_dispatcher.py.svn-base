
from threading import Thread
from pydssim.util.log.message_logger import MessageLogger

class MessageDispatcher():
    
    def __init__(self, peer):
        self.initialize(peer)
    
    def initialize(self, peer):
        self.__peer = peer
        self.__messageHandlers = {}
        self.__logger = MessageLogger()
        self.__logger.resgiterLoggingInfo("Initialize MessageHamdles pid  %s of peer %s "%(self.__class__.__name__,self.__peer.getURN()))
    
    def getMessageHandlers(self):
        return self.__messageHandlers
    
    def registerMessageHandler(self, messageHandler):
        if self.__messageHandlers.has_key(messageHandler.getCanID()):
            raise StandardError()
        self.__messageHandlers[messageHandler.getCanID()] = messageHandler
        return self.__messageHandlers[messageHandler.getCanID()]
    
    
    def countMessageHandlers(self):
        return len(self.__messageHandlers)
    
    def hasTypeMessage(self,msgType):
        
        if self.__messageHandlers.has_key(msgType):
            return True
        else:
            return False    
        
        
    def unregisterMessageHandler(self, messageName):
        if not self.__messageHandlers.has_key(messageName):
            raise StandardError()
        messageHandler = self.__messageHandlers[messageName]
        del self.__messageHandlers[messageName]
        return messageHandler
    
    def executeHandleMessage(self,messageName,peerConn,data):
        if not self.__messageHandlers.has_key(messageName):
            raise StandardError()
        handler = self.__messageHandlers[messageName]
        handler.executeHandler(peerConn,data)
#       
        return handler
    
    def handleMessage(self, messageName):
        if not self.__messageHandlers.has_key(messageName):
            raise StandardError()
        return self.__messageHandlers[messageName]
        
    
    
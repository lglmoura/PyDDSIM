from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
from pydssim.util.logger import Logger
from sets import ImmutableSet


class AbstractProtocol(Protected):
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self):
        self.__peer = None
        self.__messageHandlers = {}
    
    def registerMessageHandler(self, messageHandler):
        self.__messageHandlers[messageHandler.getMessageName()] = messageHandler
    
    def unregisterMessageHandler(self, messageName):
        pass
    
    @public    
    def sendMessage(self, message):
        raise NotImplementedError()
    
    @public
    def receiveMessage(self, message):
        raise NotImplementedError()
    
    @public
    def advertise(self, element, advertisementType):
        raise NotImplementedError()
    
    @public
    def setPeer(self, peer):
        self.__peer = peer
        return self.__peer
    
    @public
    def getPeer(self):
        return self.__peer
    
    @public
    def connect(self, priority):
        raise NotImplementedError()
    
    @public
    def disconnect(self, priority):
        raise NotImplementedError()
    
    @public
    def clone(self):
        raise NotImplementedError()
    
        
    @public
    def getMessageHandlers(self):
        return ImmutableSet(self.__messageHandlers.values())
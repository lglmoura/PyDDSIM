from pydssim.util.interface import Interface

class IP2PProtocol(object):
    
    __metaclass__ = Interface
    
    def __init__(self):
        raise NotImplementedError()
    
    def sendMessage(self, message):
        raise NotImplementedError()
    
    def receiveMessage(self, message):
        raise NotImplementedError()
    
    def advertise(self, element, advertisementType):
        raise NotImplementedError()
    
    def setPeer(self, peer):
        raise NotImplementedError()
    
    def getPeer(self):
        raise NotImplementedError()
    
    def connect(self, priority):
        raise NotImplementedError()
    
    def disconnect(self, priority):
        raise NotImplementedError()
    
    def clone(self):
        raise NotImplementedError()
    
       
    def getMessageHandlers(self):
        raise NotImplementedError()
from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public

class AbstractAdvertisement(Protected):
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, name, peer, elementId, resources={}, type):
        self.__name = name
        self.__elementId = elementId
        self.__peer = peer
        self.__resources = resources
        self.__type = type
    
    @public
    def getName(self):
        return self.__name
    
    @public
    def getElementId(self):
        return self.__elementId
    
    @public
    def getResources(self):
        return self.__resources
    
    @public
    def getType(self):
        return self.__type
    
    @public
    def getPeer(self):
        return self.__peer
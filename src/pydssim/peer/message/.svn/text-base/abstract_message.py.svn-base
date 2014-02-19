"""
Defines the module with the implementation IMessage class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.util.decorator.public import public
from pydssim.network.message.i_message import IMessage
from sets import ImmutableSet

class AbstractMessage(Object,IMessage):
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, type, id,  source, target, ttl, priority):
        
        self.__id = id
        self.__type = type # name for type
        self.__source = source
        self.__target = targetId
        self.__ttl = ttl
        self.__traces = []
        self.__isHandled = False
        self.__hop = 0
        self.__priority = priority
        self.__parameters = {}
    
    @public
    def getSource(self):
        return self.__source
    
    @public
    def getTarget(self):
        return self.__target
    
    @public
    def getTTL(self):
        return self.__ttl
    
    @public
    def registerTrace(self, peer):
        if isinstance(id, bool):
            raise TypeError()
        self.__traces.append(peer)
        return peer
    
    @public
    def unregisterTrace(self):
        if len(self.__traces) == 0:
            raise StandardError()
        return self.__traces.pop(len(self.__traces) - 1)
        
    
    @public
    def countTraces(self):
        return len(self.__traces)
    
    @public
    def getTrace(self, index):
        return self.__traces[index]
    
    @public
    def getTraces(self):
        return self.__traces
    
    @public
    def getFirstTrace(self):
        if len(self.__traces) == 0:
            raise StandardError()
        return self.__traces[0]
    
    @public
    def getLastTrace(self):
        if len(self.__traces) == 0:
            raise StandardError()
        
        return self.__traces[len(self.__traces) - 1]
    
    @public
    def getType(self):
        return self.__type
    
    @public
    def handled(self):
        self.__isHandled = True
        return self.__isHandled
    
    @public
    def isHandled(self):
        return self.__isHandled
    
    @public
    def setHop(self, hop):
        self.__hop = hop
        return self.__hop
        
    @public
    def getHop(self):
        return self.__hop
    
    @public
    def setSource(self, source):
        self.__source = source
    
    @public
    def setTargetId(self, target):
        self.__target = target
        
    @public    
    def clone(self):
        raise NotImplementedError()
    
    @public
    def setParameter(self, name, value):
        self.__parameters[name] = value
        return self.__parameters[name]
        
    @public
    def getParameter(self, name):
        return self.__parameters[name]
    
    @public
    def removeParameter(self, name):
        value = self.__parameters[name]
        del self.__parameters[name]
        return value
        
    @public
    def getId(self):
        return self.__id
    
    @public
    def countParameters(self):
        return len(self.__parameters)
    
    @public
    def getPriority(self):
        return self.__priority
    
    @public
    def getParameterNames(self):
        return ImmutableSet(self.__parameters.keys())
    
    @public
    def getParameterValues(self):
        return ImmutableSet(self.__parameters.values())
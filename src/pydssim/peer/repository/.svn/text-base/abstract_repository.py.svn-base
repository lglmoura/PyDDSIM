
from sets import ImmutableSet
#from pydssim.util.logger import Logger
from pydssim.util.log.repository_logger import RepositoryLogger
from pydssim.util.decorator.public import  createURN
from random import random,randint
from multiprocessing import Semaphore

class AbstractRepository():
    
    def __init__(self, peer):
        raise NotImplementedError()
    
    def initialize(self, peer,typeRepository):
        
        self.__uuid = createURN(typeRepository)
        self.__typeRepository = typeRepository
        self.__peer = peer
        self.__elements = {}
        RepositoryLogger()
        RepositoryLogger().resgiterLoggingInfo("Initialize Repository URN  %s of peer %s "%(self.__class__.__name__,self.__peer.getURN()))
        #Logger().resgiterLoggingInfo("Initialize Repository URN  %s of peer %s "%(self.__class__.__name__,self.__peer.getURN()))
        
   
    def addElement(self, element):
        
        key = element.getUUID()
        #if not self.__elements.has_key(key):
        self.__elements[key] = element
        
        RepositoryLogger().resgiterLoggingInfo("Add Service %s  in Repository URN  %s of peer %s "%(element.getUUID(),self.__class__.__name__,self.__peer.getURN()))
        
        return element
    
    
    def hasElement(self,key):
        return self.__elements.has_key(key)
    
    def removeElement(self, element):
        key = element.getUUID()
        if not self.__elements.has_key(key):
            raise StandardError()
        if self.__elements[key] > 0:
            del self.__elements[element]
            
        return element
    
   
    def countElements(self):
        return len(self.__elements)
    
   
    def getElements(self):
        return self.__elements
    
    
    def listAllElements(self):
        
        for element in self.getElements().values():
            print element.getUUID()
        
    def getTypeRepository(self):
        return self.__typeRepository
    
    def getPeer(self):
        return self.__peer
    
    def getUUID(self):
        return self.__uuid
    
    def getElementID(self, Id):
        
        #semaphore = Semaphore()
        #semaphore.acquire()
        element = self.__elements[Id]
        #semaphore.release()
        return element
    
    def getRandonElement(self):
       
        return self.getElementID(self.__elements.keys()[randint(0,self.countElements()-1)])
    
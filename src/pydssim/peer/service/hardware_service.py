'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.peer.service.abstract_service import AbstractService

from random import randint
import uuid

class Hardware(AbstractService):
    '''
    classdocs
    '''

    def __init__(self,pid ,resource='',size= randint(1,100000),sharePercente = randint(10,90),description='hardware',availabity=True):
        '''
        Constructor
        '''
        self.initialize(pid, resource,size,sharePercente,description,availabity)
       
        
    def initialize(self, pid,resource,size,sharePercente,description,availabity):
        
        AbstractService.initialize(self, pid,resource,description,availabity)
        
        self.__size = size
        self.__shareSize = self.__size*(sharePercente/100)
        self.__quantity = sharePercente
        
  
    def getSize(self):
        return self.__size
    
    
    def getshareSize(self):
        return self.__shareSize   
    
    
    def getQuantity(self):
        return self.__quantity 
    
    
    def setSize(self,size):
        self.__size = size
        return self.__size
    
    
    def setshareSize(self,shareSize):
        self.__shareSize = shareSize
        return self.__shareSize   
    
    
    def getQuantity(self,quantity):
        self.__quantity = quantity
        return self.__quantity    
            
        
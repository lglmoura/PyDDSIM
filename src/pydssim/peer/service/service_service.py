'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.peer.service.abstract_service import AbstractService
import uuid 

class Service(AbstractService):
    
    
    def __init__(self,pid ,resource='',description='service',availabity=True):
        '''
        Constructor
        '''
        self.initialize(pid, resource,description,availabity)
        
    def initialize(self, pid,resource,description,availabity):
        AbstractService.initialize(self, pid,resource,description,availabity)
            
    
    
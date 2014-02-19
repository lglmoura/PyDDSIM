'''
Created on Sep 10, 2009

@author: gustavo
'''


from random import randint
from pydssim.util.resource_maps import *
from pydssim.util.logger import *
from time import ctime
from pydssim.peer.resource.hardware_resource import Hardware 
from pydssim.peer.resource.abstract_resource import AbstractResource
from pydssim.peer.resource.service_resource import Service
from pydssim.peer.repository.service_repository import ServiceRepository
from pydssim.util.decorator.public import public, createURN
from pydssim.util.protected import Protected
import uuid

def createURN(type):
    
    return "urn:"+type+":id:"+uuid.uuid1().__str__()
    

def teste(t1=createURN("testesteste"),t2=randint(0,10),t3="t3",t4="t4"):
    print t1,t2,t3,t4

def get(tam=3):    
    optionMap   = [ServiceMap(),HardwareMap()]
    optionClass = [Service,Hardware]
   
    
    for i in range(0,tam):
        option = randint(0,1)
        resourceMap = ResourceMap(optionMap[option])
     
        map = resourceMap.Map()
        concept = map.keys()[randint(0, len(map.keys()) - 1)]
        initial = randint(0, (len(map[concept])/2) - 1)
        end = randint((len(map[concept])/2), len(map[concept]) - 1)
              
        print 'id %d conce %s initial %d End %d' % (i,concept,initial,end)  
        
        for ix in range(initial, end):
            service = optionClass[option](pid=createURN("peer"),resource=map[concept][ix])
                        
            print service.getUUID(),service.getResource()
            #print map[concept][ix] 

def get2(tam=5):    
    optionMap   = [ServiceMap(),HardwareMap()]
    optionClass = [Service,Hardware]
   
    
    for i in range(0,randint(1,tam)):
        option = randint(0,1)
        resourceMap = ResourceMap(optionMap[option])
     
        map = resourceMap.Map()
        
        concept = map.keys()[randint(0, len(map.keys()) - 1)]
        resour  = randint(0, (len(map[concept]) - 1))
       
              
        print 'id %d conce %s resour %d rrr %s' % (i,concept,resour,map[concept][resour])  
                
        service = optionClass[option](pid=createURN("peer"),resource=map[concept][resour])
                    
        #print service.getUUID(),service.getResource(),service.testedemetodo()
        #print map[concept][ix]
            
             
if __name__ == '__main__':
    
    get2(7)
    
    
   
    '''
        
    print createURN("peer"),[teste(t4="teste4")]    
    t1 = {10:11,20:21}
    t1[30]=31
    t1[40]=41
    i =  randint(0, len(t1.keys()) - 1)
    print "key ", t1.keys()#[randint(0, len(t1.keys()) - 1)]
    print t1.values()#[randint(0, len(t1.keys()) - 1)]
    print "key ", t1.keys()[i],"valor ",t1[t1.keys()[i]]
                   
    for h in t1.values():
        print h
    
    
    print "tam", len(t1.values())
    
    '''
        
  
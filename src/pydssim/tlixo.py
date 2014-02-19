'''
Created on 22/08/2009

@author: LGustavo
'''

from random import randint
from pydssim.util.resource_maps import *
from pydssim.util.logger import *
from time import ctime
from pydssim.peer.resource.hardware_resource import Hardware 
from pydssim.peer.resource.abstract_resource import AbstractResource
from pydssim.peer.resource.service_resource import Service
from pydssim.peer.repository.service_repository import ServiceRepository
from pydssim.util.protected import Protected
import uuid

def get():    
    op = [ServiceMap(),HardwareMap()]
    for i in range(0,3):
        resources = ResourceMap(op[randint(0,1)])
     
        map = resources.Map()
        concept = map.keys()[randint(0, len(map.keys()) - 1)]
        initial = randint(0, (len(map[concept])/2) - 1)
        end = randint((len(map[concept])/2), len(map[concept]) - 1)
        print 'id %d conce %s indtial %d End %d' % (i,concept,initial,end)  
        
        for ix in range(initial, end):
            print map[concept][ix] 
            
            
def testUUID(set =uuid.uuid1()):
    Logger().resgiterLoggingError("testeUUID")
    print set
    
if __name__ == '__main__':
    m1 = Logger()
    m1.resgiterLoggingError("Star Simulation")
    m2 = Logger('w')
    m2.resgiterLoggingInfo("Star Simulation2")
    m3 = Logger()
    m3.resgiterLoggingError("Star Simulation3")
    m4 = Logger('w')
    m4.resgiterLoggingInfo("Star Simulation4")
    m4.resgiterLoggingInfo("teste4")
    # Obtm um datatime da data e hora atual
    #hoje = datetime.today()
    #print ctime() 
    h = Hardware(1,"memoria")
   
    print h.getPID(), h.getUUID()
    
    r = Service(111,1111)
    
  
    
    if  isinstance(r, Hardware):
        print "h"
        
    if  isinstance(r, AbstractResource):
        print "AR"     
    
    
    sr = ServiceRepository(111)
    sr.addElement(h)
    sr.addElement(r)
    x= sr.getElements()
    for key in x.keys():
        print 'key=%s, valeu=%s'%(key,x[key])
    
    
    testUUID("tet")
    #get()    
  
        
    '''
    map = FolksonomyMap()
     
    id = 1  
    concept = map.mapping.keys()[randint(0, len(map.mapping.keys()) - 1)]
    initial = randint(0, (len(map.mapping[concept])/2) - 1)
    end = randint((len(map.mapping[concept])/2), len(map.mapping[concept]) - 1)
    print 'id %d conce %s indtial %d End %d' % (id,concept,initial,end)  
    
    for ix in range(initial, end):
        print map.mapping[concept][ix]

    ''' 

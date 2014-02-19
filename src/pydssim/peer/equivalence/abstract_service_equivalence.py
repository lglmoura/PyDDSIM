'''
Created on 28/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''


from pydssim.util.decorator.public import  createURN
from pydssim.util.data_util import randomDate
from random import random,randint
from pydssim.util.log.equivalence_logger import EquivalenceLogger


class AbstractServiceEquivalence():
    '''
    classdocs
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def initialize(self, resource):
      
        self.__uuid = resource.getUUID()
        self.__resource = resource
         
        self.__equivalences = {}
        
         
    def getResourceDescription(self):
        return self.__resource.getDescription()
      
    def getResourceUUID(self):
        return self.__resource.getUUID()
    
    def getResourceTag(self):
        return self.__resource.getTag()
    
    def getResource(self):
        return self.__resource.getResource()
    
    def getResourceS(self):
        return self.__resource
    
    
    def getEquivalences(self):
        return self.__equivalences
    
         
    def getUUID(self):
        return self.__uuid
    
    
    def getAllEquivalenceInPeriod(self,periodStart,periodEnd):
        return dict([(equivalenceID,equivalence) for equivalenceID, equivalence in self.getEquivalences().iteritems()
                      if(equivalence.getPeriodStart() <=periodStart) and (equivalence.getPeriodEnd()>= periodEnd)])
        
   
     
    def hasEquivalencesForTag(self,serviceTag,periodStart,periodEnd):
       
        return dict([(equivalenceID,equivalence) for equivalenceID, equivalence in self.getEquivalences().iteritems()
                      if (equivalence.getEquivalence().getResourceTag() == serviceTag) and 
                         (equivalence.getPeriodStart() <=periodStart) and (equivalence.getPeriodEnd()>= periodEnd)]) 
     
    def hasEquivalences(self,recourseEquivalence,periodStart,periodEnd):
       
        return dict([(equivalenceID,equivalence) for equivalenceID, equivalence in self.getEquivalences().iteritems()
                      if (equivalence.getEquivalence().getResourceUUID() == recourseEquivalence) and 
                         (equivalence.getPeriodStart() <=periodStart) and (equivalence.getPeriodEnd()>= periodEnd)])
    
    
    def addEquivalence(self, equivalence):
        
        key = equivalence.getUUID()
        if not self.__equivalences.has_key(key):
            recourseEquivalentes = self.hasEquivalences(equivalence.getEquivalence().getResourceUUID(),equivalence.getPeriodStart(),equivalence.getPeriodEnd())
            if (not recourseEquivalentes):
                self.__equivalences[key] = equivalence
        
        #EquivalenceLogger().resgiterLoggingInfo("Add Service %s  in Repository URN  %s of peer %s "%(equivalence.getUUID(),self.__class__.__name__,self.__peer.getURN()))
        
        return equivalence
    
    
    def removeEquivalence(self, equivalence):
        key = equivalence.getUUID()
        if not self.__equivalences.has_key(key):
            raise StandardError()
        if self.__equivalences[key] > 0:
            del self.__equivalences[equivalence]
            
        return equivalence
    
    def lookForEquivalence(self,uuid):
        pass
    
    def countEquivalences(self):
        return len(self.__equivalences)
    
   
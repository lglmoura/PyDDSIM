'''
Created on 28/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''


from pydssim.util.decorator.public import  createURN


class AbstractService():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def initialize(self, peer,resource, description='',availabity=True):
      
        self.__uuid = createURN(description)
        self.__resource = resource
        self.__tag      = resource    
        self.__description = description
        self.__sourcePeer = peer
        
        self.__availability = availabity
       
        self.__sharePeriod = {}
        
       
    def getResource(self):
        return self.__resource
    
    def getTag(self):
        return self.__tag
    
    
    def getSharePeriod(self):
        return self.__sharePeriod
    
        
    def hasSharePeriods(self,periodStart,periodEnd):
       
        return dict([(sharePeriodID,sharePeriod) for sharePeriodID, sharePeriod in self.__sharePeriod.iteritems()
                      if (sharePeriod.getPeriodStart() <=periodStart) and (sharePeriod.getPeriodEnd()>= periodEnd)])
     
     
    def hasSharePeriodswithQuantity(self,periodStart,periodEnd,quantity,metric):
        '''
        print "###############  abs service ",periodStart,periodEnd,quantity,metric
        
        for sh in self.getSharePeriod().values():
            print "## ",sh.getService().getResource(),sh.getPeriodStart(),sh.getPeriodEnd(),sh.getQuantity(),sh.getMetric(),sh.getStatus()
            if (sh.getPeriodStart() <=periodStart)and (sh.getPeriodEnd()>= periodEnd)  and  (sh.getQuantity() >=int(quantity)) and (sh.getMetric() == metric):
                print "##  ====",sh.getService().getResource(),sh.getPeriodStart(),sh.getPeriodEnd(),sh.getQuantity(),sh.getMetric(),sh.getStatus()
        
        
        '''
        
        return dict([(sharePeriodID,sharePeriod) for sharePeriodID, sharePeriod in self.getSharePeriod().iteritems()
                      if (sharePeriod.getPeriodStart() <=periodStart) and (sharePeriod.getPeriodEnd()>= periodEnd) and
                         (sharePeriod.getQuantity() >=int(quantity)) and (sharePeriod.getMetric() == metric)])
     
    def addSharePeriod(self, sharePeriod):
        
        key = sharePeriod.getUUID()
        if not self.__sharePeriod.has_key(key):
            sharePeriods = self.hasSharePeriods(sharePeriod.getPeriodStart(),sharePeriod.getPeriodEnd())
            if (not sharePeriods):
                self.__sharePeriod[key] = sharePeriod
        
        #EquivalenceLogger().resgiterLoggingInfo("Add Service %s  in Repository URN  %s of peer %s "%(equivalence.getUUID(),self.__class__.__name__,self.__peer.getURN()))
        
        return sharePeriod    
    
    def updateSharePeriod(self,sharePeriod):
        key = sharePeriod.getUUID()
        self.__sharePeriod[key] = sharePeriod
        
    def setResource(self,resource):
        self.__resource = resource
        return self.__resource
    
     
    def getDescription(self):
        return self.__description
    
    
    def getPeer(self):
        return self.__sourcePeer
    
    
    def setPeer(self,peer):
        self.__sourcePeer = peer
        return self.__sourcePeer
    
     
    def getAvailability(self):
        return self.__availability
    
    
    def getPeriod(self):
        return self.__period
    
    
    def getUUID(self):
        return self.__uuid
    
    
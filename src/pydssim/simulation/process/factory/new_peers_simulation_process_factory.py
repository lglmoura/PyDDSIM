"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

import threading
from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory

from pydssim.peer.default_peer import DefaultPeer
from pydssim.peer.portal_peer import PortalPeer
from pydssim.peer.abstract_peer import AbstractPeer
from pydssim.peer.trust.direct_trust import DirectTrust
from pydssim.peer.trust.abstract_trust import AbstractTrust
from pydssim.peer.equivalence.service_equivalence import ServiceEquivalence
from pydssim.peer.equivalence.equivalence import Equivalence
from pydssim.peer.repository.equivalence_repository import EquivalenceRepository

from pydssim.util.resource_maps import *
from pydssim.peer.service.hardware_service import Hardware 
from pydssim.peer.service.abstract_service import AbstractService
from pydssim.peer.service.service_service import Service
from pydssim.peer.service.shared_period import SharePeriod
import time
from pydssim.util.log.simulation_process_logger import SimulationProcessLogger
from SimPy.Simulation import *
from random import random,randint,shuffle

from pydssim.util.data_util import randomDate,strTime
import uuid

from datetime import datetime

class NewPeersSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"NEW DEDAULTPEER PROCESS FACTORY",6)
        
    def createSharePeriods(self,peer,service,dateTimeStart,dateTimeStop):
        
        
        for  countShare in range(1,10):
        
            periodStart = randomDate(dateTimeStart,dateTimeStop, random())
            periodEnd = randomDate(periodStart,dateTimeStop, random())
            quantity = 10 #randint(1,10)
            
            service.addSharePeriod(SharePeriod(service,periodStart,periodEnd,quantity,peer.getURN()))
        
        
       
    
    def createServices(self,peer,tam,dateTimeStart,dateTimeStop):
        
        ''' change resource '''
        
        optionMap   = [ServiceMap(),HardwareMap()]
        optionClass = [Service,Hardware]
       
        
        
        #for i in range(0,randint(1,tam)):
        for i in range(0,4):
            
            option = randint(0,1)
            
           
            
            resourceMap = ResourceMap(optionMap[option])
            #resourceMap = ResourceMap(optionMap[1])
         
            map = resourceMap.Map()
            
            concept = map.keys()[randint(0, len(map.keys()) - 1)]
            resour  = randint(0, (len(map[concept]) - 1))
                    
            service = optionClass[option](peer.getPID(),resource=map[concept][resour])
            
            has = False
            for vServices in peer.getServices().getElements().values():
                
                if service.getResource() == vServices.getResource():
                    has = True
                    break
            if not has:
                self.createSharePeriods(peer,service,dateTimeStart,dateTimeStop)
                peer.getServices().addElement(service)
                
    
    def createTrust(self,peer,peers,transactionNumber,dateTimeStart,dateTimeStop):
       
        keys= peers.keys()
        shuffle(keys)
           
        #directTrust = peer.getDirectTrust()
        directTrust = peer.getTrustManager().getDirectTrust()
        status = [True,False]
        for i in keys: 
        
            peerID,peerN = i, peers[i]
                             
            services = peerN.getServices()
           
            for countEle in range(0,randint(0,services.countElements())):
                
                element = services.getRandonElement()
                #print element.getUUID(),element.getResource()
                
                for countTrans in range(0,randint(0,transactionNumber)):
                    rating= random()
                    
                    
                    period = randomDate(dateTimeStart,dateTimeStop, random())
                   
                    option = randint(0,1)
                    
                    directTrust.addElement(DirectTrust(peerID,element.getUUID(),element.getTag(),AbstractTrust.DIRECT,rating,period,status[option]))
     
     
         
    
    def createEquivalence(self,peer,dateTimeStart,dateTimeStop):
       
       # Procura nao fazer para todos
       
        equivalenceRepository = peer.getEquivalenceRepository()
                         
        services = peer.getServices()
        
        tam = services.countElements()
       
        if tam <2:
            return   
        
       
        for countEle in range(0,tam):
            
            
            serviceS = services.getElements().values()[countEle]
            
            if equivalenceRepository.hasElement(serviceS.getUUID()):
               
                service = equivalenceRepository.getElementID(serviceS.getUUID())
            else:
                
                service = ServiceEquivalence(serviceS)    
                
            for z in range(countEle+1,tam):
                
                serviceE = services.getElements().values()[z]
                
                if equivalenceRepository.hasElement(serviceE.getUUID()):
                     
                     equivalenceS = equivalenceRepository.getElementID(serviceE.getUUID())
                else:
                     
                     equivalenceS = ServiceEquivalence(serviceE)
                #print "aqui"
            
                #print "e --->",countEle,z,equivalenceS.getResource(),equivalenceS.getResourceUUID()
                serviceQuantity = 5 #randint(1,10)
                equivalenceQuantity = 5 #randint(1,10)
                
                periodStar = randomDate(dateTimeStart,dateTimeStop, random())
                periodEnd = randomDate(periodStar,dateTimeStop, random())
                
                #equivalence = Equivalence(service,serviceQuantity,equivalenceS,equivalenceQuantity,periodStar,periodEnd)
                
                #print "aa", service,serviceQuantity,equivalenceS,equivalenceQuantity,periodStar,periodEnd
                
                service.addEquivalence(Equivalence(service,serviceQuantity,equivalenceS,equivalenceQuantity,periodStar,periodEnd))
                equivalenceS.addEquivalence(Equivalence(equivalenceS,equivalenceQuantity,service,serviceQuantity,periodStar,periodEnd))        
                
                equivalenceRepository.addElement(service)
                equivalenceRepository.addElement(equivalenceS)
            
    def showEquivalence(self,peer):
        
        print "----------------peer--------"
        for serviceE in peer.getEquivalenceRepository().getElements().values():
            print "-----------equiva--------------"
            for equiva in serviceE.getEquivalences().values():
                print equiva.getService().getResource(),equiva.getEquivalence().getResource(),equiva.getPeriodAll()
                               
    def factorySimulationProcess(self):
        
        
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
       
        port = 4000
      
        portalID = network.getPortalID()
      
        while ( ( peer_number < simulation.getNetwork().getPeers())):# and ( simulation.getSimInstance().now() < simulation.getSimulationTime() )):
            peer_number+=1 
            
            urn = "urn:peer:"+uuid.uuid1().__str__()
            logMsg = "Factoring Process %s => Simulation Time %10.2f making peer number : %s id %s" % (self.getName(),simulation.getSimInstance().now() ,peer_number, urn) 
            SimulationProcessLogger().resgiterLoggingInfo(logMsg)
            #print logMsg
            peer = DefaultPeer(urn,port)
           
            self.createServices(peer,simulation.getResourcePeer(),simulation.getTransactionDateTimeStart(),simulation.getTransactionDateTimeStop())
            #print peer.getServices().getElements().keys()
            
            self.createEquivalence(peer, simulation.getTransactionDateTimeStart(),simulation.getTransactionDateTimeStop())
            
            self.createTrust(peer,network.getPeersFromLayout(peer),simulation.getTransactionNumber(),simulation.getTransactionDateTimeStart(),simulation.getTransactionDateTimeStop())
            
            network.addPeer(peer)
            peer.connectPortal(portalID)
            
            t = threading.Thread( target = peer.mainLoop,
                              args = [] )
            t.start()
           
            port += 1
           
            print "Defau Peer = %s = %s = %s = %s"%(datetime.today(), peer.getPID(),peer_number,simulation.getSimInstance().now())
                  
            randa = randint(5,10)# 
            yield hold, self, randa
            
       
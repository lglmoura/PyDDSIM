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

from pydssim.util.log.simulation_process_logger import SimulationProcessLogger
from SimPy.Simulation import *
from random import random,randint,shuffle

from pydssim.util.data_util import randomDate,strTime
import uuid

from datetime import datetime

class OutPeersSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

     

    def __init__(self):
        self.__active =36
        AbstractSimulationProcessFactory.initialize(self,"OUT SIMPLEPEER PROCESS FACTORY",self.__active)
                                   
    def factorySimulationProcess(self):
        
               
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
       
                
        while network.countPeers > 1:# and ( simulation.getSimInstance().now() < simulation.getSimulationTime() )):
         
            
            
            logMsg = "Factoring Process %s => Simulation Time %10.2f" % (self.getName(),simulation.getSimInstance().now()) 
            SimulationProcessLogger().resgiterLoggingInfo(logMsg)
             
            peer = network.getRandonPeer()
            
            
            if peer.getPeerType() != AbstractPeer.SIMPLE:
                continue
            
            #randa =simulation.getNetwork().getNewPeerTime()*random()
            peer_number+=1
            peer.setShutdown()
            print "Remov Peer = %s = %s = %s = %s"%(datetime.today(), peer.getPID(),peer_number, simulation.getSimInstance().now())
            randa = randint(4,8)*6
            yield hold, self, randa
            
        
       
            
      
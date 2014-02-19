"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

import threading
from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory
from datetime import datetime
from pydssim.peer.super_peer import SuperPeer

from pydssim.peer.abstract_peer import AbstractPeer

from pydssim.util.log.simulation_process_logger import SimulationProcessLogger
from SimPy.Simulation import *
from random import random
import uuid

class OutSuperPeersSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

   
    def __init__(self):
        self.__active = 600
        AbstractSimulationProcessFactory.initialize(self,"OUT SIMPLEPEER PROCESS FACTORY",self.__active)
                                   
    def factorySimulationProcess(self):
        
               
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
       
                
        while network.countPeers > 1:# and ( simulation.getSimInstance().now() < simulation.getSimulationTime() )):
         
            
            peer_number+=1
            logMsg = "Factoring Process %s => Simulation Time %10.2f" % (self.getName(),simulation.getSimInstance().now()) 
            SimulationProcessLogger().resgiterLoggingInfo(logMsg)
             
            peer = network.getRandonPeer()
            
            
            if peer.getPeerType() == AbstractPeer.SIMPLE:
                continue
            
            #randa =simulation.getNetwork().getNewPeerTime()*random()
            print "OUT SIMPLEPEER PROCESS FACTORY Peer ----------------------------------------------------> ",datetime.today(), peer.getPID(),peer.getPeerType(),peer_number
            peer.setShutdown()
            network.removePeer(peer)
            yield hold, self, self.__active
            
        
       
            
      
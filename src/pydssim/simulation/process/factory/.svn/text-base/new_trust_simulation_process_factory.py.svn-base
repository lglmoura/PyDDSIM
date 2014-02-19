"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

import threading
from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory

from pydssim.peer.super_peer import SuperPeer

from pydssim.peer.abstract_peer import AbstractPeer

from pydssim.util.logger import Logger
from SimPy.Simulation import *
from random import random
import uuid

class NewTrustSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"NEW TRUST PROCESS FACTORY")
        
   
    def factorySimulationProcess(self):
        
               
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        
        
        while ( simulation.getSimInstance().now() < simulation.getSimulationTime() ):
           
            
          
            logMsg = "Factoring Process %s => Simulation Time %10.2f making : %s" % (self.getName(),simulation.getSimInstance().now()) 
            Logger().resgiterLoggingInfo(logMsg)
                                
            peerSource = network.getRandonPeer()  
            peerTarget = network.getRandonPeer() 
            
            peerSource.connectPortal(portalID,1)
            
            
           
            yield hold, self, simulation.getNetwork().getNewPeerTime()*random()*(peer_number)#*2)
            
        
       
            
      
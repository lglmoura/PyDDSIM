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


from SimPy.Simulation import *
from random import random
import uuid

class NewPortalPeersSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"NEW PORTAL PEER PROCESS FACTORY",0)
        
   
    def factorySimulationProcess(self):
        
      
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
       
        ###
        startPort = 2000
       
      
        portal = PortalPeer( "urn:portalpeer:"+uuid.uuid1().__str__(), startPort)
        
        network.setPortalID(portal.getPID())
        tp = threading.Thread( target = portal.mainLoop,
                              args = [] )
        tp.start()
        yield hold, self, simulation.getNetwork().getNewPeerTime()*random()
             
            
        
       
       
            
      
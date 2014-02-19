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
import time

from pydssim.peer.abstract_peer import AbstractPeer

from pydssim.util.log.simulation_process_logger import SimulationProcessLogger
from SimPy.Simulation import *
from random import random, seed, expovariate, normalvariate,randint


import uuid

class NewSuperPeersSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"NEW SUPERPEER PROCESS FACTORY",3)
        
   
    def factorySimulationProcess(self):
        
               
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
       
        ###
        port = 3000
      
        portalID = network.getPortalID()
        totalSP  = simulation.getNetwork().getPeers()/simulation.getNetwork().getMaxNeighbor()
        
        while (( peer_number < totalSP )):# and ( simulation.getSimInstance().now() < simulation.getSimulationTime() )):
            peer_number+=1 
            
            
           
            urn = "urn:superpeer:"+uuid.uuid1().__str__()
            logMsg = "Factoring Process %s => Simulation Time %10.2f making peer number : %s id %s" % (self.getName(),simulation.getSimInstance().now() ,peer_number, urn) 
            SimulationProcessLogger().resgiterLoggingInfo(logMsg)
            #print logMsg
            peer = SuperPeer(urn,port,simulation.getNetwork().getMaxNeighbor())
           
           
            network.addPeer(peer)
            
            peer.connectPortal(portalID,1)
           
            print "Super Peer = %s = %s = %s = %s"%(datetime.today(), peer.getPID(),peer_number, simulation.getSimInstance().now())
            
            t = threading.Thread( target = peer.mainLoop,
                              args = [] )
            t.start()
                      
            port += 1
           
           
            
            randa = randint(55,65)#
          
            yield hold,self,randa
           
           
        
       
            
      
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
from pydssim.util.log.simulation_process_logger import SimulationProcessLogger
from SimPy.Simulation import *
from random import random,randint,shuffle
from pydssim.peer.trading.abstract_trading import AbstractTrading
from pydssim.util.data_util import randomDate,strTime
import uuid

class NewTradingSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"NEW TRADING PROCESS FACTORY",120)
        
    
   
                               
    def factorySimulationProcess(self):
        
        peers = {}
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        
        contt = 0
        while  (simulation.getSimInstance().now() < simulation.getSimulationTime()):
             
            #yield hold, self, simulation.getNetwork().getNewPeerTime()*random()
            peer = network.getRandonPeer()
            
            if peer.getPID() in peers.keys():
                if  peers[peer.getPID()] < 4:
                    
                    peers[peer.getPID()] += 1
                else:
                    print "tttttttttttttttttttttttttttttttttttt" 
                    continue    
            else:
                
                peers[peer.getPID()] = 0
                         
            
            services = peer.getServices()
            
            if services.countElements()>=2:
                urn = "urn:trading:"+uuid.uuid1().__str__()
                logMsg = "Factoring Process %s => Simulation Time %10.2f making  : id %s" % (self.getName(),simulation.getSimInstance().now() , urn) 
                SimulationProcessLogger().resgiterLoggingInfo(logMsg)
                
                periodStart = randomDate(simulation.getTransactionDateTimeStart(),simulation.getTransactionDateTimeStop(), random())
                periodEnd = randomDate(periodStart,simulation.getTransactionDateTimeStop(), random()) 
                serviceQuantity = 5#randint(1,10)
            
            
                service = services.getElements().values()[randint(0,services.countElements()-1)]
                print "New Trading Service -> ",datetime.today(),peer.getPID(),service.getResource(),peers[peer.getPID()],contt
                contt+=1
             
                peer.getTradingManager().creatTradingService(service,periodStart,periodEnd,serviceQuantity,AbstractTrading.CLIENT)
                yield hold, self, 24
            
              
              
            
       
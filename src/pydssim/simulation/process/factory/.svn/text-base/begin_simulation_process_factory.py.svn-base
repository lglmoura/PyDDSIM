"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory
from pydssim.util.decorator.public import public
from pydssim.simulation.process.begin_simulation_process import BeginSimulationProcess
from pydssim.util.log.simulation_process_logger import SimulationProcessLogger
from SimPy.Simulation import *


class BeginSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"BEGIN SIMULATION PROCESS FACTORY",0)
        
    
    @public
    def factorySimulationProcess(self):
        
        SimulationProcessLogger().resgiterLoggingInfo("Factoring Process %s"%self.getName())
        yield hold, self, 1
        process = BeginSimulationProcess()
        process.start()
        
       
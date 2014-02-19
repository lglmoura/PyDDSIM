"""
@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 6/07/2009
"""
from pydssim.simulation.process.abstract_simulation_process import AbstractSimulationProcess
from pydssim.util.decorator.public import public
from pydssim.util.log.simulation_process_logger import SimulationProcessLogger

class BeginSimulationProcess(AbstractSimulationProcess):
    """
    Defines the implementation of BeginSimulationProcess
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 6/07/2009
    """

    def __init__(self,simInstance=None):
        AbstractSimulationProcess.initialize(self, "BEGIN_SIMULATION_PROCESS",simInstance)
        
    @public
    def start(self):
        
        SimulationProcessLogger().resgiterLoggingInfo("Start %s"%self.getIdentifier())
        
        return 
    
    
        
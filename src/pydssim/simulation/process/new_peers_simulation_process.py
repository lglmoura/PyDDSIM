"""
@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 6/07/2009
"""
from pydssim.simulation.process.abstract_simulation_process import AbstractSimulationProcess
from pydssim.util.decorator.public import public
from pydssim.util.logger import Logger

class NewPeersSimulationProcess(AbstractSimulationProcess):
    """
    Defines the implementation of BeginSimulationProcess
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 6/07/2009
    """

    def __init__(self,simInstance=None):
        AbstractSimulationProcess.initialize(self, "NEW PEERS SIMULATION PROCESS",simInstance)
        
    @public
    def start(self):
        
        Logger().resgiterLoggingInfo("Start %s"%self.getIdentifier())
        
        return 
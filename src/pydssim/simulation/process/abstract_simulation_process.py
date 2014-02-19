"""
Defines the module with the implementation of AbstractSimulationEvent class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 5/07/2009
"""

from pydssim.simulation.process.i_simulation_process import ISimulationProcess

from SimPy.Simulation import Process
from pydssim.util.log.simulation_process_logger import SimulationProcessLogger

class AbstractSimulationProcess(Process,ISimulationProcess):
    """
    Abstract class that implemenents the ISimulationEvent interface.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 5/07/2009
    """
      
    def __init__(self):
        raise NotImplementedError()
    
  
    def initialize(self, identifier, simInstance, peer=None, priority=0):
        """
        Initializes the object.
        @param identifier: identifier of simulation event
        @type identifier: str
        @param peerId: peerId of simulation event
        @type peerId: int
        @param priority: priority of simulation event.
        @type priority: int
        @rtype: None
        @note: All simulation events are initialized as unhandled.
        """
        
        Process.__init__(self, identifier,simInstance)
        
        self.__identifier = identifier
        self.__peer = peer
        self.__priority = priority
        self.__isIdentified = False
        SimulationProcessLogger().resgiterLoggingInfo("Initialize Simulation Process => %s"%self.__identifier)
    
    
    def getIdentifier(self):
        return self.__identifier

   
    def getPeer(self):
        return self.__peer

    
    def getPriority(self):
        return self.__priority
    
    
    def identified(self):
        self.__isIdentified = True

   
    def isIdentified(self):
        return self.__isIdentified
    
   
    def start(self):
        """
        Template method to implement specific algorithm for handling a given simulation process.
        
        @note: The visibility of this operation is protected.
        @rtype: NoneType
        """
        raise NotImplementedError()
    
    def __eq__(self, other):
        if not other:
            return False
        return self.__identifier == other.getIdentifier() and self.__peerId == other.getPeerId() and self.__priority == other.getPriority()
    
   
    
    
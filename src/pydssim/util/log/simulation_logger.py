"""
Defines the module with the implementation AbstractPeer class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.util.log.abstract_logger import AbstractLogger


import traceback

class SimulationLogger(AbstractLogger):
    """
    Implements the basic functions of a peer.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self, fileMode='a',logFileName = 'simulation_logger__file.log'):
        
              
        AbstractLogger.initialize(self,fileMode,logFileName)
        
              
            
        
    

        
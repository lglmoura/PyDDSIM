"""
Defines the module with the specification of ISimulationEvent interface.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 5/07/2009
"""

class ISimulationProcess(object):
    """
    Defines the interface of simulation event objects.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 5/07/2009
    """

    def __init__(self):
        raise NotImplementedError()
    
    def getIdentifier(self):
        """
        Gets the Identifier of simulation event.
        @return: Returns the str object.
        @rtype: str
        """
        raise NotImplementedError()
    
    def getPriority(self):
        """
        Gets the priority of simulation event.
        @return: Returns the int object.
        @rtype: int
        """
        raise NotImplementedError()
    
    def getPeerId(self):
        """
        Gets the peerId of simulation event.
        @return: Returns the int object
        @rtype: int
        """
        raise NotImplementedError()
    
    def identified(self):
        """
        Changes the state of simulation event to handled.
        @return: Returns the bool object.
        @rtype: bool
        """
        raise NotImplementedError()
    
    def isIdentified(self):
        """
        Verifies the state of simulation event, returns true if simulation event already was
        handled, else returns false.
        @return: Returns the bool object.
        @rtype: bool
        """
        raise NotImplementedError()
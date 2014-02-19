"""
Defines the module with the specification of ISimulation interface.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@vocs.ufrj.br 
@since: 5/07/2009
"""

class ISimulation(object):
    """
    Defines the interface of simulation objects.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
   
    """
    
    def __init__(self):
        raise NotImplementedError()
    
    def start(self):
        """
        Executes the simulation.
        @rtype: NoneType
        """
        raise NotImplementedError()
    
    
    
    def initializeNetwork(self, peers ,newPeerTime ,neighbors):
        raise NotImplementedError() 
    
    def configure(self):
        """
        Configures the simulation.
        @rtype: NoneType
        """
        raise NotImplementedError()
    
    def stop(self):
        """
        Stops the simulation.
        @rtype: NoneType
        """
        raise NotImplementedError()
    
    def getSimulationTime(self):
        """
        Gets the during time of simulation.
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def setSimulationTime(self, simulationTime):
        """
        Sets a time of simulation.
        @param simulationTime: an int
        @type simulationTime: int
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def setNetwork(self, Network):
        """
        Sets a  network object.
        @param Network: an INetwork
        @type Network: INetwork
        @return: an INetwork
        @rtype: INetwork
        """
        raise NotImplementedError()
    
    def getNetwork(self):
        """
        Gets a peer-to-peer network object.
        @return: an INetwork
        @rtype: INetwork
        """
        raise NotImplementedError()
    
    def getCurrentSimulationTime(self):
        """
        Gets the current time of simulation.
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
      
       
    def setCurrentSimulationTime(self, currentSimulationTime):
        """
        Sets the current time of simulation.
        @param currentSimulationTime: an int
        @type currentSimulationTime: int
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
   
    
    def getSimInstance(self):
        """
        Sets a simulator.
        @return: an ISimulator
        @rtype: ISimulator
        """
        raise NotImplementedError()
    
    
    
    def addSimulationProcessFactory(self, simulationProcessFactory):
        """
        Adds a simulation event generator.
        @param simulationEventGenerator: an ISimulationProcessFactory
        @return: a ISimulationEventGenerator
        @rtype: ISimulationEventGenerator
        """
        raise NotImplementedError()
    
    def removeSimulationProcessFactory(self, simulationProcessFactory):
        """
        Removes a simulation Process Factorys.
        @param simulationEventGenerator: an ISimulationProcessFactory
        @return: a ISimulationEventGenerator
        @rtype: ISimulationEventGenerator
        """
        raise NotImplementedError()
    
    def getSimulationProcessFactorys(self):
        """
        Gets a list of simulation Process Factoryss.
        @return: a list
        @rtype: list
        """
        raise NotImplementedError()
    
    def countSimulationProcessFactorys(self):
        """
        Counts simulation Process Factoryss.
        @return: a int
        @rtype: int
        """
        raise NotImplementedError()
    
    def initializeNetwork(self ,peers ,newPeerTime):
        """
        create network.
        @return: a int
        @rtype: int
        """
        raise NotImplementedError()
    
     
    def getResourcePeer(self):
        raise NotImplementedError()

    
    def setResourcePeer(self, resourcePeer):
        
        raise NotImplementedError()

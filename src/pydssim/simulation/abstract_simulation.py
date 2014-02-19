"""
Defines the module with the implementation of AbstractSimulation class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@vocs.ufrj.br 
@since: 5/07/2009
"""


from pydssim.simulation.i_simulation import ISimulation
from multiprocessing import Semaphore
from SimPy.Simulation import Simulation
from pydssim.util.log.simulation_logger import SimulationLogger

import time

class AbstractSimulation(ISimulation):
    """
    Defines the interface of simulation objects.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
   
    """
     
    def __init__(self):
        raise NotImplementedError()

    
    def initialize(self):
        """
        Initializes the object.
        @rtype: NoneType
        """
        self.__simInstance = Simulation() 
        self.__simInstance.initialize()

        
        self.__simulationTime = 0
        self.__currentSimulationTime = 0
        self.__network = None
        self.__simulationProcessFactory = []
        self.__resourcePeer = 0
        self.__transactionNumber = 0
        self.__transactionDateTimeStart = ""
        self.__transactionDateTimeStop = ""
        #self.__logger = SimulationLogger() 
        #self.__logger.resgiterLoggingInfo("Create Simulation ")
        SimulationLogger().resgiterLoggingInfo("Create Simulation ")
    
   
    def initializeNetwork(self, peers ,newPeerTime ,neighbors):
        raise NotImplementedError() 

    
    def addSimulationProcessFactory(self, simulationProcessFactory):
       
        if simulationProcessFactory in self.__simulationProcessFactory:
            return None
        simulationProcessFactory.setSimulation(self)
        simulationProcessFactory.initializeProcess()
        self.__simulationProcessFactory.append(simulationProcessFactory)
       
        
        return self.__simulationProcessFactory[self.__simulationProcessFactory.index(simulationProcessFactory)]

    
    def removeSimulationProcessFactory(self, simulationProcessFactory):
       
        if not simulationProcessFactory in self.__simulationProcessFactory:
            return None
        self.__simulationProcessFactory.remove(simulationProcessFactory)
        return simulationProcessFactory

    
    def getSimulationProcessFactorys(self):
        return self.__simulationProcessFactory

    
    def countSimulationProcessFactorys(self):
        return len(self.__simulationProcessFactory)
    
       
    def configure(self):
        raise NotImplementedError()
    
        
    def getNetwork(self):
        return self.__network
    
    
    def setNetwork(self, network):
        
        self.__network = network
        self.__network.setSimulation(self)
        return self.__network
    
       
    def getSimulationTime(self):
        return self.__simulationTime

    
    def setSimulationTime(self, simulationTime):
        
        self.__simulationTime = simulationTime
        return self.__simulationTime
    
        
    def getResourcePeer(self):
        return self.__resourcePeer

    
    def setResourcePeer(self, resourcePeer):
        
        self.__resourcePeer = resourcePeer
        return self.__resourcePeer
    
    def getTransactionNumber(self):
        return self.__transactionNumber
    
    def setTransactionNumber(self, number):
        
        self.__transactionNumber = number
        return self.__transactionNumber
    
    def getTransactionDateTimeStart(self):
        return self.__transactionDateTimeStart
    
    def setTransactionDateTimeStart(self, date):
        
        self.__transactionDateTimeStart = date
        return self.__transactionDateTimeStart
    
    
    def getTransactionDateTimeStop(self):
        return self.__transactionDateTimeStop
    
    def setTransactionDateTimeStop(self, date):
        
        self.__transactionDateTimeStop = date
        return self.__transactionDateTimeStop
    
    def getCurrentSimulationTime(self):
        semaphore = Semaphore()
        semaphore.acquire()
        time = self.__currentSimulationTime
        semaphore.release()
        return time
    
    
    def setCurrentSimulationTime(self, currentSimulationTime):
       
        semaphore = Semaphore()
        semaphore.acquire()
        self.__currentSimulationTime = currentSimulationTime
        semaphore.release()
        return self.__currentSimulationTime
    
    
    def getSimInstance(self):
        return self.__simInstance
    
        
    
    def start(self):
        
        mySim = self.getSimInstance()
        
        SimulationLogger().resgiterLoggingInfo("Start Simulation ")
        #Logger().resgiterLoggingInfo("Start Simulation ")
        factoryProcess = 0
        for factory in self.__simulationProcessFactory:
            print factory.getName()
            mySim.activate( factory, factory.factorySimulationProcess(),at=factory.getActive()) 
            
            factoryProcess +=1
            
            
        mySim.simulate( until = self.getSimulationTime() )    
        return factoryProcess
       
    
    
    def stop(self):
        raise NotImplementedError()
       
    
    
    simInstance = property(getSimInstance, None, None, None)
   
    simulationTime = property(getSimulationTime, setSimulationTime, None, None)
    
    currentSimulationTime = property(getCurrentSimulationTime, setCurrentSimulationTime, None, None)
   
    network = property(getNetwork, setNetwork, None, None)
    
    
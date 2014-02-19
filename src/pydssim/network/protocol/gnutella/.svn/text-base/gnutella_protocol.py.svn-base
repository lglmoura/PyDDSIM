from pydssim.network.protocol.abstract_protocol import AbstractProtocol
from pydssim.util.decorator.public import public
from multiprocessing import Semaphore
from random import randint
from pydssim.network.message.message_manager import MessageManager
from pydssim.network.protocol.gnutella.message.advertise_content_message import AdvertiseContentMessage
from pydssim.network.protocol.gnutella.dispatcher.advertise_content_message_handler import AdvertiseContentMessageHandler

class GnutellaProtocol(AbstractProtocol):
    
    def __init__(self):
        self.initialize()
    
    @public
    def setPeer(self, peer):
        self.registerMessageHandler(AdvertiseContentMessageHandler(peer))
        return AbstractProtocol.setPeer(self, peer)
    
    @public    
    def sendMessage(self, message):
        self.getPeer().getNetowk().dispatchMessage(message)
        
    
    @public
    def receiveMessage(self, message):
        if self.getPeer().getId() == message.getTargetId():
            Logger().resgiterLoggingInfo("receive Message from PID = "+message.getSourceID())
            dispatcher = self.getPeer().getMessageDispatcher()
            dispatcher.handleMessage(message)
            
        #else:
           #pass
            
    @public
    def advertise(self, element, advertisementType):
        peer = self.getPeer()
        network = peer.getNetwork()
        simulation = network.getSimulation()
        neighbors = self.network.getNeighbors(peer)
        for n in neighbors:
            message = AdvertiseContentMessage(MessageManager().getMessageId(), peer.getId(), n, simulation.getNumberOfHops(), simulation.getSimulationCurrentTime())
            message.registerTrace(self.getPeer().getId())
            message.setParameter("contentId", element.getId())
            #message.setParameter("folksonomies", element.getFolksonomies())
            message.setParameter("type", advertisementType)
            peer.send(message)
    
    @public
    def connect(self, priority):
        sem = Semaphore()
        sem.acquire()
        if self.getPeer().isConnected():
            return
        network = self.getPeer().getNetwork()
        
        node = None
        if netowork.countNodes() > 0:
            idx = randint(0, network.countNodes() - 1)
            graph = network.getGraph()
            node = graph.keys()[idx]
        
        network.addNode(self.getPeer())
        if node:
            network.createConnection(self.getPeer(), node)
            
        self.getPeer().connected()
        # randon time for disconnect
        disconnectionTime = randint(3600, 28800)
        self.getPeer().setDisconnectionTime(disconnectionTime)
        
        sem.release()
    
    @public
    def disconnect(self, priority):
        sem = Semaphore()
        sem.acquire()
        if not self.getPeer().isConnected():
            return
        
        network = self.getPeer().getNetwork()
        neighbors = network.getNeighbors(self.getPeer())
        if len(neighbors) > 0:
            for n in neighbors:
                network.removeConnection(self.getPeer(), n)
                self.getPeer().disconnected()
        else:
            self.getPeer().disconnected()
            
    @public
    def clone(self):
        raise NotImplementedError()
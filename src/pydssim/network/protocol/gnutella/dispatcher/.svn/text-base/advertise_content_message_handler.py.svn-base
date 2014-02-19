from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.decorator.public import public
from pydssim.network.advertisement.content_advertisement import ContentAdvertisement
from pydssim.network.route import ContentRoute

class AdvertiseContentMessageHandler(AbstractMessageHandler):
    
    def __init__(self, peer):
        self.initialize("ADVERTISE_CONTENT", peer)
    
    @public
    def clone(self):
        return AdvertiseContentMessageHandler(self.getPeer())
    
    def executeHandler(self):
        message = self.getMessage()
        if message.getHop() < message.getTTL():
            peer = self.getPeer()
            
            advertisement = ContentAdvertisement(message.getTraces()[0], message.getParameter("contentId"), message.getParameter("resources"), message.getParameter("type"))
                    
            neighbor = peer.getNeighbor(message.getSourceId())
            neighbor.addRoute(ContentRoute(advertisement.getElementId(), message.getTraces()))
            
            neighbors = peer.getNeighbors()
            
            for n in neighbors:
                if n.getId() in message.getTraces():
                    continue
                
                msg = message.clone()
                msg.registerTrace(peer.getId())
                msg.setHop(msg.getHop() + 1)
                msg.setTargetId(n.getId())
                msg.setSourceId(peer.getId())
                peer.send(msg)
            
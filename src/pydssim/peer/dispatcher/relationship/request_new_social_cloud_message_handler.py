from pysocialsim.p2p.dispatcher.abstract_message_handler import AbstractMessageHandler
from pysocialsim.base.decorator.public import public
from pysocialsim.p2p.message.relationship.accept_new_social_cloud_message import AcceptNewSocialCloudMessage
from pysocialsim.p2p.message.message_manager import MessageManager
from pysocialsim.p2p.profile.default_social_cloud_view import DefaultSocialCloudView
from random import randint

class RequestNewSocialCloudMessageHandler(AbstractMessageHandler):
    
    def __init__(self, peer):
        self.initialize("REQUEST_NEW_SOCIAL_CLOUD", peer)
        
    @public
    def clone(self):
        return RequestNewSocialCloudMessageHandler(self.getPeer())
    
    def executeHandler(self):
        peer = self.getPeer()
        content = peer.getContent(self.getP2PMessage().getParameter("elementId"))
        network  = peer.getP2PNetwork()
        simulation = network.getSimulation()
        
        cloud = DefaultSocialCloudView(randint(0, 99999999999999), 0)
  
        message = AcceptNewSocialCloudMessage(MessageManager().getMessageId(), peer.getId(), self.getP2PMessage().getSourceId(), simulation.getNumberOfHops(), simulation.getSimulationCurrentTime())
        message.setParameter("elementId", self.getP2PMessage().getParameter("elementId"))
        message.setParameter("type", self.getP2PMessage().getParameter("type"))
        message.setParameter("sourceCloudId", cloud.getId())
        message.setParameter("contentSize", content.getSize())
        
        profile = peer.getProfile()
        profile.addSocialCloud(cloud)
        
        peer.send(message)
        
from pysocialsim.p2p.dispatcher.abstract_message_handler import AbstractMessageHandler
from pysocialsim.base.decorator.public import public
from pysocialsim.p2p.profile.default_social_cloud_view import DefaultSocialCloudView
from random import randint
from pysocialsim.p2p.message.relationship.share_content_social_cloud_message import ShareContentSocialCloudMessage
from pysocialsim.p2p.message.message_manager import MessageManager
from pysocialsim.p2p.profile.default_social_retationship import DefaultSocialRelationship

class AcceptNewSocialCloudMessageHandler(AbstractMessageHandler):
    
    def __init__(self, peer):
        self.initialize("ACCEPT_NEW_SOCIAL_CLOUD", peer)
        
    @public
    def clone(self):
        return AcceptNewSocialCloudMessageHandler(self.getPeer())
    
    def executeHandler(self):
        peer = self.getPeer()
        network = peer.getP2PNetwork()
        simulation = network.getSimulation()
        
        cloud = DefaultSocialCloudView(randint(0, 99999999999999), self.getP2PMessage().getParameter("contentSize") * 2)
        
        if peer.getDiskSpace() > cloud.getSharedDiskSpace():
            peer.setDiskSpace(peer.getDiskSpace() - cloud.getSharedDiskSpace())
            
            relationship = DefaultSocialRelationship(self.getP2PMessage().getSourceId(), self.getP2PMessage().getParameter("sourceCloudId"))
            cloud.addSocialRelationship(relationship)
            
            profile = peer.getProfile()
            profile.addSocialCloud(cloud)
            
            message = ShareContentSocialCloudMessage(MessageManager().getMessageId(), self.getPeer().getId(), self.getP2PMessage().getSourceId(), simulation.getNumberOfHops(), simulation.getSimulationCurrentTime())
            message.setParameter("elementId", self.getP2PMessage().getParameter("elementId"))
            message.setParameter("type", self.getP2PMessage().getParameter("type"))
            message.setParameter("sourceCloudId", cloud.getId())
            message.setParameter("targetCloudId", self.getP2PMessage().getParameter("sourceCloudId"))
            message.setParameter("sharedDiskSpace", cloud.getSharedDiskSpace())
            
            peer.send(message)
        else:
            print "Falhou"
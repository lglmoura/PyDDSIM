from pysocialsim.p2p.dispatcher.abstract_message_handler import AbstractMessageHandler
from pysocialsim.base.decorator.public import public
from pysocialsim.p2p.profile.default_social_retationship import DefaultSocialRelationship
from pysocialsim.p2p.message.relationship.accept_share_content_social_cloud_message import AcceptShareContentSocialCloudMessage
from pysocialsim.p2p.message.message_manager import MessageManager

class ShareContentSocialCloudMessageHandler(AbstractMessageHandler):
    
    def __init__(self, peer):
        self.initialize("SHARE_CONTENT_SOCIAL_CLOUD", peer)
        
    @public
    def clone(self):
        return ShareContentSocialCloudMessageHandler(self.getPeer())
    
    def executeHandler(self):
        peer = self.getPeer()
        network = peer.getP2PNetwork()
        simulation = network.getSimulation()
        
        content = peer.getContent(self.getP2PMessage().getParameter("elementId"))
        profile = peer.getProfile()
        
        if self.getP2PMessage().getParameter("sharedDiskSpace") >= content.getSize():
            cloud = profile.getSocialCloud(self.getP2PMessage().getParameter("targetCloudId"))
            
            relationship = DefaultSocialRelationship(self.getP2PMessage().getSourceId(), self.getP2PMessage().getParameter("sourceCloudId"))
            cloud.addSocialRelationship(relationship)
            
            cloud.addSharedContent(content.clone())
            content.addOwner(self.getP2PMessage().getSourceId())
            
            message = AcceptShareContentSocialCloudMessage(MessageManager().getMessageId(), self.getPeer().getId(), self.getP2PMessage().getSourceId(), simulation.getNumberOfHops(), simulation.getSimulationCurrentTime())
            message.setParameter("elementId", self.getP2PMessage().getParameter("elementId"))
            message.setParameter("type", self.getP2PMessage().getParameter("type"))
            message.setParameter("sourceCloudId", cloud.getId())
            message.setParameter("targetCloudId", self.getP2PMessage().getParameter("sourceCloudId"))
            message.setParameter("content", content)
            
            peer.send(message)
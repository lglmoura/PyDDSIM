from pysocialsim.p2p.dispatcher.abstract_message_handler import AbstractMessageHandler
from pysocialsim.base.decorator.public import public

class AcceptShareContentSocialCloudMessageHandler(AbstractMessageHandler):
    
    def __init__(self, peer):
        self.initialize("ACCEPT_SHARE_CONTENT_SOCIAL_CLOUD", peer)
    
    @public
    def clone(self):
        return AcceptShareContentSocialCloudMessageHandler(self.getPeer())
    
    def executeHandler(self):
        peer = self.getPeer()
        network = peer.getP2PNetwork()
        simulation = network.getSimulation()
        
        profile = peer.getProfile()
        cloud = profile.getSocialCloud(self.getP2PMessage().getParameter("targetCloudId"))
        content = self.getP2PMessage().getParameter("content")
        
        cloud.addSharedContent(content)
        peer.addContent(content)
        
        print self.getMessageName()
from pydssim.network.advertisement.abstract_advertisement import AbstractAdvertisement

class ContentAdvertisement(AbstractAdvertisement):
    
    def __init__(self, peer, elementId, resources, type):
        self.initialize("CONTENT_ADVERTISEMENT", peer, elementId, resources, type)
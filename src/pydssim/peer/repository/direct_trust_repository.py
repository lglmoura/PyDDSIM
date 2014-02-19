from pydssim.peer.repository.abstract_repository import AbstractRepository

class DirectTrustRepository(AbstractRepository):
    
    def __init__(self, peer):
        self.initialize(peer,typeRepository="DirectTrustRepository")
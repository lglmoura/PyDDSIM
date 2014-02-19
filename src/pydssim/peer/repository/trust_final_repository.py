from pydssim.peer.repository.abstract_repository import AbstractRepository

class TrustFinalRepository(AbstractRepository):
    
    def __init__(self, peer):
        self.initialize(peer,typeRepository="TrustFinalRepository")
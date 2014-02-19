from pydssim.peer.repository.abstract_repository import AbstractRepository

class SharedRecourceRepository(AbstractRepository):
    
    def __init__(self, peer):
        self.initialize(peer,typeRepository="SharedRecourceRepository")
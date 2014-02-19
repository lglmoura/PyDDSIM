from pydssim.network.message.abstract_message import AbstractMessage

class DefaultMessage(AbstractMessage):
    
    def __init__(self, id, source, target, ttl, priority):
        self.initialize("DEFAULT",  source, target, ttl, priority)
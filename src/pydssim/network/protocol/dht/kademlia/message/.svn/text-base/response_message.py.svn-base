'''
Created on 21/12/2009

@author: LGustavo
'''
from pydssim.network.protocol.dht.kademlia.message.message import Message

class ResponseMessage(Message):
    """ Message containing the result from a successful RPC request """
    def __init__(self, rpcID, nodeID, response):
        Message.__init__(self, rpcID, nodeID)
        self.response = response

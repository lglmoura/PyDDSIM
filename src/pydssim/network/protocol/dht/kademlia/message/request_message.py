'''
Created on 21/07/2009

@author: LGustavo
'''


import hashlib
import random
from pydssim.network.protocol.dht.kademlia.message.message import Message

class RequestMessage(Message):
    """ Message containing an RPC request """
    def __init__(self, nodeID, method, methodArgs, rpcID=None):
        if rpcID == None:
            hash = hashlib.sha1()
            hash.update(str(random.getrandbits(255)))  
            rpcID = hash.digest()
        Message.__init__(self, rpcID, nodeID)
        self.request = method
        self.args = methodArgs

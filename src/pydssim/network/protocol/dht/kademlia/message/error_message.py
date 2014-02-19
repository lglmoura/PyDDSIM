'''
Created on 21/12/2009

@author: LGustavo
'''

from pydssim.network.protocol.dht.kademlia.message.message import Message
from pydssim.network.protocol.dht.kademlia.message.response_message import ResponseMessage

class ErrorMessage(ResponseMessage):
    """ Message containing the error from an unsuccessful RPC request """
    def __init__(self, rpcID, nodeID, exceptionType, errorMessage):
        ResponseMessage.__init__(self, rpcID, nodeID, errorMessage)
        if isinstance(exceptionType, type):
            self.exceptionType = '%s.%s' % (exceptionType.__module__, exceptionType.__name__)
        else:
            self.exceptionType = exceptionType

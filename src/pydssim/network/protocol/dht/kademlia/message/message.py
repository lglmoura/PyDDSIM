'''
Created on 21/07/2009

@author: LGustavo
'''

class Message(object):
    """ Base class for messages - all "unknown" messages use this class """
    def __init__(self, rpcID, peerID):
        self.id = rpcID
        self.peerID = peerID
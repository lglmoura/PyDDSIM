'''
Created on 19/12/2009

@author: LGustavo
'''

class Neighbor(object):
    """ Encapsulation for remote neighbor
    
    This class contains information on a single remote neighbor, and also
    provides a direct RPC API to the remote peer which it represents
    """
    def __init__(self, id, ipAddress, udpPort, networkProtocol, firstComm=0):
        self.id = id
        self.address = ipAddress
        self.port = udpPort
        self._networkProtocol = networkProtocol
        self.commTime = firstComm
        
    def __eq__(self, other):
        if isinstance(other, Neighbor):
            return self.id == other.id
        elif isinstance(other, str):
            return self.id == other
        else:
            return False
    
    def __ne__(self, other):
        if isinstance(other, Neighbor):
            return self.id != other.id
        elif isinstance(other, str):
            return self.id != other
        else:
            return True
        
    def __str__(self):
        return '<%s.%s object; IP address: %s, UDP port: %d>' % (self.__module__, self.__class__.__name__, self.address, self.port)
    
    def __getattr__(self, name):
        """ This override allows the host peer to call a method of the remote
        peer (i.e. this neighbor) as if it was a local function.
        
        For instance, if C{remotePeer} is a instance of C{Neighbor}, the
        following will result in C{remotePeer}'s C{test()} method to be
        called with argument C{123}::
         remotePeer.test(123)
        
        Such a RPC method call will return a Deferred, which will callback
        when the contact responds with the result (or an error occurs).
        This happens via this contact's C{_networkProtocol} object (i.e. the
        host Peer's C{_protocol} object).
        """
        def _sendRPC(*args, **kwargs):
            return self._networkProtocol.sendRPC(self, name, args, **kwargs)
        return _sendRPC

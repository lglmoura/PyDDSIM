'''
Created on 21/07/2009

@author: LGustavo
'''


class IMessageTranslator(object):
    """ Interface for RPC message translators/formatters
    
    Classes inheriting from this should provide a translation services between
    the classes used internally by this Kademlia implementation and the actual
    data that is transmitted between peers.
    """
    def fromPrimitive(self, msgPrimitive):
        """ Create an RPC Message from a message's string representation
        
        @param msgPrimitive: The unencoded primitive representation of a message
        @type msgPrimitive: str, int, list or dict
        
        @return: The translated message object
        @rtype: dht.kademlia.message.Message
        """
    
    def toPrimitive(self, message):
        """ Create a string representation of a message
        
        @param message: The message object
        @type message: message.Message
        
        @return: The message's primitive representation in a particular
                 messaging format
        @rtype: str, int, list or dict
        """
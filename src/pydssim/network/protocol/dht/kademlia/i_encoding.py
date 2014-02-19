'''
Created on 20/07/2009

@author: LGustavo
'''

class IEncoding(object):
    """ Interface for RPC message encoders/decoders
    
    All encoding implementations used with this library should inherit and
    implement this.
    """
    def encode(self, data):
        """ Encode the specified data
        
        @param data: The data to encode
                     This method has to support encoding of the following
                     types: C{str}, C{int} and C{long}
                     Any additional data types may be supported as long as the
                     implementing class's C{decode()} method can successfully
                     decode them.
        
        @return: The encoded data
        @rtype: str
        """
    def decode(self, data):
        """ Decode the specified data string
        
        @param data: The data (byte string) to decode.
        @type data: str
        
        @return: The decoded data (in its correct type)
        """